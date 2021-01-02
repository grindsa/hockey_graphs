import React from 'react';
import { Calendar } from './calendar';

export class ChangeMatchday extends React.Component {
  /* this class displays a header allowing matchday changes */

  constructor(props) {
    super(props);
    this.state = {
      showCalendar: 'none',
    };
    this.toggleCalendar = this.toggleCalendar.bind(this);
  }

  async toggleCalendar(){
      let { showCalendar } = this.state;
      await this.setState({ showCalendar: showCalendar === 'none' ? 'block' : 'none' });
  }

  render(){
    return(
      <div className="w3-container w3-padding scolor">
        <div className="w3-col w3-left w3-padding-top" style={{width:'10%'}}>
            <i className="w3-padding-top fa fa-calendar-day w3-large fa-lg w3-margin-left w3-left" onClick={() => this.toggleCalendar()}/>
            <Calendar
              display={this.state.showCalendar}
              toggleCalendar={this.toggleCalendar}
              language={this.props.language}
              matchdaylist={this.props.matchdaylist}
              current={this.props.current}
              date={this.props.date}
              handleDayClick = {this.props.handleDayClick}
            />
        </div>
        <div className="w3-col w3-center" style={{width:'80%'}}>
        <HeadBar next={this.props.next}  previous={this.props.previous} date={this.props.date} onChangeMatchDay={this.props.onChangeMatchDay} />
        </div>
        <div className="w3-col w3-left" style={{width:'10%'}}></div>
    </div>
    )
  }
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
