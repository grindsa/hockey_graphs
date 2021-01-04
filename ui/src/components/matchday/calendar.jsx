import React, {useState, useEffect} from 'react';
import PropTypes from "prop-types";
import DayPicker from 'react-day-picker';
import 'react-day-picker/lib/style.css';

export const Calendar = (props) => {
  /* a component to show a localized calendar */

  const [firstMatchDay, setFirstMatchDay] = useState(null)
  const [lastMatchDay, setLastMatchDay] = useState(null)
  const [disabledDaysList, setDisabledDaysList] = useState([])
  // const [showCalendar, setShowCalendar] = useState(false)

  const createdisabledDaysList = (matchdaylist) => {
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

  useEffect(() => {
    if (props.matchdaylist.length > 0){
      setFirstMatchDay(props.matchdaylist[0])
      setLastMatchDay(props.matchdaylist[props.matchdaylist.length - 1])
      // setShowCalendar(true)
      const disabledDaysList = createdisabledDaysList(props.matchdaylist.sort())
      setDisabledDaysList(disabledDaysList)
    }
  }, [props.matchdaylist])

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
  // const FIRST_DAY_OF_WEEK = { DE: 1};
  const LABELS = {DE: { nextMonth: 'Nächster Monat', previousMonth: 'vorheriger Monat' }};
  return (
    <div className="w3-modal" style={{display: props.display}}>
      <div className="w3-modal-content w3-white w3-card-4" style={{width: 350}}>
        <div className="w3-container">
          <span className="w3-button pcolor w3-display-topright" onClick={() => props.toggleCalendar()}>&times;</span>
          <DayPicker
            locale={props.language}
            months={MONTHS[props.language]}
            weekdaysLong={WEEKDAYS_LONG[props.language]}
            weekdaysShort={WEEKDAYS_SHORT[props.language]}
            firstDayOfWeek={1}
            labels={LABELS[props.language]}
            fromMonth={new Date(firstMatchDay)}
            toMonth={new Date(lastMatchDay)}
            month={new Date(props.current)}
            selectedDays={[new Date(props.current)]}
            disabledDays={disabledDaysList}
            onDayClick={props.handleDayClick}
          />
        </div>
      </div>
    </div>
  )
}

Calendar.propTypes = {
    current: PropTypes.string,
    display: PropTypes.string.isRequired,
    language: PropTypes.string.isRequired,
    matchdaylist: PropTypes.array.isRequired,
    handleDayClick: PropTypes.func.isRequired,
    toggleCalendar: PropTypes.func.isRequired,
};
