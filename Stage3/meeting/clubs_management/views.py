from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.contrib import messages
from django.db import connection, transaction
from datetime import timedelta

from .models import Meeting, Club, Room
from .forms import MeetingForm, ReportForm


def meeting_list(request):
    """
    Display a list of all meetings.
    Utilizes select_related to optimize database queries by prefetching related Club and Room objects.
    """
    meetings = Meeting.objects.select_related('club', 'room').all()
    return render(request, 'clubs_management/meeting_list.html', {'meetings': meetings})


def meeting_edit(request, meeting_id=None):
    """
    Add a new meeting or edit an existing one.
    Implements transaction management to ensure atomicity of the save operation.
    """
    if meeting_id:
        meeting = get_object_or_404(Meeting, pk=meeting_id)
    else:
        meeting = None

    if request.method == "POST":
        form = MeetingForm(request.POST, instance=meeting)
        if form.is_valid():
            try:
                with transaction.atomic():
                    form.save()
            except Exception as e:
                # Handle the exception and provide feedback
                messages.error(request, f"An error occurred while saving the meeting: {e}")
            else:
                messages.success(request, "Meeting saved successfully.")
                return redirect(reverse('meeting_list'))
    else:
        form = MeetingForm(instance=meeting)

    return render(request, 'clubs_management/meeting_edit.html', {'form': form})


def meeting_delete(request, meeting_id):
    """
    Delete a specific meeting.
    Ensures that deletion is performed via POST request to prevent accidental deletions.
    Implements transaction management to ensure atomicity of the delete operation.
    """
    meeting = get_object_or_404(Meeting, pk=meeting_id)

    if request.method == "POST":
        try:
            with transaction.atomic():
                meeting.delete()
        except Exception as e:
            # Handle the exception and provide feedback
            messages.error(request, f"An error occurred while deleting the meeting: {e}")
        else:
            messages.success(request, "Meeting deleted successfully.")
            return redirect(reverse('meeting_list'))

    # Render confirmation page for deletion (if needed)
    return render(request, 'clubs_management/meeting_confirm_delete.html', {'meeting': meeting})


def meeting_report(request):
    """
    Generate a report of meetings based on filter conditions.
    Uses Raw SQL to perform aggregate calculations.
    Implements exception handling to manage potential errors during query execution.
    """
    form = ReportForm(request.GET or None)
    report_data = None

    if form.is_valid():
        # Get filter conditions from the form
        start_date = form.cleaned_data.get('start_date')
        end_date = form.cleaned_data.get('end_date')
        club = form.cleaned_data.get('club')
        room = form.cleaned_data.get('room')

        # Prepare SQL query with parameterized inputs to prevent SQL injection
        sql_query = """
            SELECT 
                AVG(EXTRACT(EPOCH FROM duration)) AS average_duration_seconds,
                AVG(invited_count) AS average_invited_count,
                AVG(accepted_count) AS average_accepted_count
            FROM clubs_management_meeting
            WHERE 1=1
        """
        params = []

        if start_date:
            sql_query += " AND date >= %s"
            params.append(start_date)
        if end_date:
            sql_query += " AND date <= %s"
            params.append(end_date)
        if club:
            sql_query += " AND club_id = %s"
            params.append(club.id)
        if room:
            sql_query += " AND room_id = %s"
            params.append(room.id)

        try:
            with transaction.atomic():
                with connection.cursor() as cursor:
                    cursor.execute(sql_query, params)
                    row = cursor.fetchone()

                if row and row[0] is not None:
                    average_duration_seconds = row[0]
                    average_duration = timedelta(seconds=average_duration_seconds)
                    hours, remainder = divmod(average_duration.total_seconds(), 3600)
                    minutes = remainder // 60
                    formatted_average_duration = f"{int(hours)}h {int(minutes)}m"
                else:
                    formatted_average_duration = "No Data"

                # Store query results in report_data
                report_data = {
                    'average_duration': formatted_average_duration,
                    'average_invited_count': row[1] if row[1] is not None else "No Data",
                    'average_accepted_count': row[2] if row[2] is not None else "No Data",
                    'average_attendance_rate': (row[2] / row[1]) if row[1] else "No Data"
                }

        except Exception as e:
            # Handle the exception and provide feedback
            messages.error(request, f"An error occurred while generating the report: {e}")

    return render(request, 'clubs_management/meeting_report.html', {
        'form': form,
        'report_data': report_data,
    })
