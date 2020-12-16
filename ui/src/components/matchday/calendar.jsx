import React from 'react';
import DayPicker from 'react-day-picker';
import 'react-day-picker/lib/style.css';

export class Calendar extends React.Component{
  /* a component to show a localized calendar */

  constructor(props) {
    super(props);
    this.state = {
      selectedMatchDay: props.date,
      lastMatchDay: null,
      firstMatchDay: null,
      showCalendar: false,
      disabledDaysList: [],
    }
  }

  componentDidMount(){
    const disabledDaysList = this.createdisabledDaysList(this.props.matchdaylist.sort())
    if (this.props.matchdaylist.length > 0){
      this.setState({
        firstMatchDay: this.props.matchdaylist[0],
        lastMatchDay: this.props.matchdaylist[this.props.matchdaylist.length - 1],
        currentMatchDay: this.props.current,
        showCalendar: true,
        disabledDaysList: disabledDaysList
      });
    }
  }

  async componentDidUpdate(prevProps){
    if (this.props.matchdaylist !== prevProps.matchdaylist) {
      const disabledDaysList = this.createdisabledDaysList(this.props.matchdaylist.sort())
      if (this.props.matchdaylist.length > 0){
        await this.setState({
          firstMatchDay: this.props.matchdaylist[0],
          lastMatchDay: this.props.matchdaylist[this.props.matchdaylist.length - 1],
          currentMatchDay: this.props.current,
          showCalendar: true,
          disabledDaysList: disabledDaysList
        });
      }
    }
  }

  createdisabledDaysList(matchdaylist){
    var disabledDaysList = []
    // first element of list with before only
    disabledDaysList.push({before: new Date(matchdaylist[0])})
    matchdaylist.forEach(function (after, index) {
        var before = matchdaylist[index+1]
        if(before){
          disabledDaysList.push({ after: new Date(after), before: new Date(before)})
        }
    });
    // last element of list if after only
    disabledDaysList.push({after: new Date(matchdaylist[matchdaylist.length - 1])})
    return disabledDaysList
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
        <div className="w3-modal-content w3-white w3-card-4" style={{width: 350}}>
          <div className="w3-container">
            <span className="w3-button pcolor w3-display-topright" onClick={() => this.props.toggleCalendar()}>&times;</span>
            <DayPicker
              locale={this.props.language}
              months={MONTHS[this.props.language]}
              weekdaysLong={WEEKDAYS_LONG[this.props.language]}
              weekdaysShort={WEEKDAYS_SHORT[this.props.language]}
              firstDayOfWeek={1}
              labels={LABELS[this.props.language]}
              fromMonth={new Date(this.state.firstMatchDay)}
              toMonth={new Date(this.state.lastMatchDay)}
              month={new Date(this.props.current)}
              selectedDays={[new Date(this.props.current)]}
              disabledDays={this.state.disabledDaysList}
              onDayClick={this.props.handleDayClick}
            />
          </div>
        </div>
      </div>
    )

  }
}
