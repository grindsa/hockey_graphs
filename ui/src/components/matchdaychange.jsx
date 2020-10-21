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
      <div className="w3-container w3-padding scolor w3-center">
        <h1>
          <i className="fa fa-calendar fa-lg w3-margin-left w3-left" onClick={() => this.toggleCalendar()}/>
          <Calendar display={this.state.showCalendar} toggleCalendar={this.toggleCalendar} language={this.props.language}/>
          <a href='#' onClick={() => this.props.onChangeMatchDay(this.props.previous)}><i className="w3-margin-right fa fa-arrow-left" /></a>
           {this.props.date}
          <a href='#' onClick={() => this.props.onChangeMatchDay(this.props.next)}><i className="w3-margin-left fa fa-arrow-right" /></a>
        </h1>
      </div>
    )
  }
}
