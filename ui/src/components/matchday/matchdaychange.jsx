import React, {useState} from 'react';
import PropTypes from "prop-types";
import { Calendar } from './calendar';

export const ChangeMatchday = (props) => {

  const [showCalendar, setShowCalendar] = useState('none')

  const toggleCalendar = () => {
    setShowCalendar(showCalendar === 'none' ? 'block' : 'none')
  }

  return(
    <div className="w3-container w3-padding scolor">
      <div className="w3-col w3-left w3-padding-top" style={{width:'10%'}}>
        <i className="w3-padding-top fa fa-calendar-day w3-large fa-lg w3-margin-left w3-left" onClick={() => toggleCalendar(event)}/>
        <Calendar
          display={showCalendar}
          toggleCalendar={toggleCalendar}
          language={props.language}
          matchdaylist={props.matchdaylist}
          current={props.current}
          date={props.date}
          handleDayClick = {props.handleDayClick}
        />
      </div>
      <div className="w3-col w3-center" style={{width:'80%'}}>
      <HeadBar next={props.next}  previous={props.previous} date={props.date} onChangeMatchDay={props.onChangeMatchDay} />
      </div>
      <div className="w3-col w3-left" style={{width:'10%'}}></div>
    </div>
  )
}

const HeadBar = (props) => {
  return(
    <h1 className='pseudohead'>
       <HeadPrevious previous={props.previous} onChangeMatchDay={props.onChangeMatchDay} />
       {props.date}
       <HeadNext next={props.next} onChangeMatchDay={props.onChangeMatchDay} />
    </h1>
  )
}

const HeadPrevious = ({previous, onChangeMatchDay}) => {
  if (previous){
    return(<a href='#' onClick={() => onChangeMatchDay(previous)}><i className="w3-margin-right fa fa-arrow-left" /></a>)
  }else{
    return(<i className="w3-margin-right fa fa-arrow-left w3-opacity-max" />)
  }
}

const HeadNext = ({next, onChangeMatchDay}) => {
  if (next){
    return(<a href='#' onClick={() => onChangeMatchDay(next)}><i className="w3-margin-left fa fa-arrow-right" /></a>)
  }else{
    return(<i className="w3-margin-left fa fa-arrow-right w3-opacity-max" />)
  }
}

ChangeMatchday.propTypes = {
    current: PropTypes.string,
    next: PropTypes.string,
    previous: PropTypes.string,
    date: PropTypes.string.isRequired,
    language: PropTypes.string.isRequired,
    matchdaylist: PropTypes.array.isRequired,
    onChangeMatchDay: PropTypes.func.isRequired,
    handleDayClick: PropTypes.func.isRequired,
};

HeadBar.propTypes = {
    date: PropTypes.string,
    next: PropTypes.string,
    previous: PropTypes.string,
    onChangeMatchDay: PropTypes.func.isRequired,
}

ChangeMatchday.propTypes = {
    onChangeMatchDay: PropTypes.func.isRequired,
}
