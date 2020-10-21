import React from 'react';
import DayPicker from 'react-day-picker';
import 'react-day-picker/lib/style.css';

export class Calendar extends React.Component{

  constructor(props) {
    super(props);
  }

  render() {

    const WEEKDAYS_SHORT = { DE: ['So', 'Mon', 'Di', 'Mi', 'Do', 'Fr', 'Sa'] }
    const MONTHS = {
      DE: [
        'Januar',
        'Februar',
        'März',
        'Аpril',
        'Маi',
        'Juni',
        'Juli',
        'Аugust',
        'September',
        'Оktober',
        'November',
        'Dezember',
      ]};

    const WEEKDAYS_LONG = { DE: ['Sonntag', 'Montag', 'Dienstag', 'Mittwoch', 'Donnerstag', 'Freitag', 'Samstag']};
    const FIRST_DAY_OF_WEEK = { DE: 1};
    const LABELS = {DE: { nextMonth: 'Nächster Monat', previousMonth: 'vorheriger Monat' }};

    return (
      <div className="w3-modal" style={{display: this.props.display}}>
        <div className="w3-modal-content w3-white">
          <div className="w3-container">
            <span className="w3-button w3-display-topright" onClick={() => this.props.toggleCalendar()}>&times;</span>
            <DayPicker
              locale={this.props.language}
              months={MONTHS[this.props.language]}
              weekdaysLong={WEEKDAYS_LONG[this.props.language]}
              weekdaysShort={WEEKDAYS_SHORT[this.props.language]}
              firstDayOfWeek={1}
              labels={LABELS[this.props.language]}
            />
          </div>
        </div>
      </div>
    )
  }
}
