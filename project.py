import sys
from functions import (
    cmd_import, cmd_insert_admin, cmd_add_venue,
    cmd_reserve_slot, cmd_cancel_reservation, cmd_update_event,
    cmd_delete_organizer, cmd_available_events, cmd_popular_event_types,
    cmd_participant_schedule, cmd_organizer_stats, cmd_venue_events,
)


def main():
    args = sys.argv[1:]
    func = args[0]

    if func == 'import':
        cmd_import(args[1])
    elif func == 'insertAdmin':
        cmd_insert_admin(int(args[1]), args[2], args[3], args[4], args[5], args[6])
    elif func == 'addVenue':
        cmd_add_venue(int(args[1]), int(args[2]), args[3].lower() == 'true')
    elif func == 'reserveSlot':
        cmd_reserve_slot(int(args[1]), int(args[2]), int(args[3]))
    elif func == 'cancelReservation':
        cmd_cancel_reservation(int(args[1]), int(args[2]), int(args[3]))
    elif func == 'updateEvent':
        cmd_update_event(int(args[1]), args[2], args[3])
    elif func == 'deleteOrganizer':
        cmd_delete_organizer(int(args[1]))
    elif func == 'availableEvents':
        cmd_available_events(args[1])
    elif func == 'popularEventTypes':
        cmd_popular_event_types(int(args[1]))
    elif func == 'participantSchedule':
        cmd_participant_schedule(int(args[1]))
    elif func == 'organizerStats':
        cmd_organizer_stats(int(args[1]))
    elif func == 'venueEvents':
        cmd_venue_events(int(args[1]))


if __name__ == '__main__':
    main()
