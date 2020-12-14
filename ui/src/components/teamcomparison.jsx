import React from 'react';
import { isMobileOnly } from 'react-device-detect';
import { Chart } from './teamcomparison/chart';
import { Selector } from './teamcomparison/selector';

import { checkTcUpdate }  from './teamcomparison/teamcomparisonstateservice.js';
import { asyncGET, isEmpty } from './sharedfunctions.js';
import { createnostatMessage } from './localization.js';

export class TeamComparison extends React.Component {

  constructor(props) {
    super(props);
    this.state = {
      teamcomparisonList: [],
      selectedstat: 0,
    };
    this.handleStatChange = this.handleStatChange.bind(this);
  }

  async componentDidMount(){
    if (this.props.teamcomparison && this.props.season) {
      // get team comparison
      const tcdic = await asyncGET(this.props.teamcomparison + '?season=' + this.props.season + '&mobile=' + isMobileOnly + '&language=' + this.props.language)
      this.setState({teamcomparisonList: tcdic});
    }
  }

  async componentDidUpdate(prevProps) {
    /* we get the url to fectch as props and monitor it here */
    const tcupdate = checkTcUpdate(this.props.teamcomparison, prevProps.teamcomparison, this.props.season, prevProps.season, this.props.language, prevProps.language)
    if (tcupdate){
        // get team comparison
        const tcdic = await asyncGET(this.props.teamcomparison + '?season=' + this.props.season + '&mobile=' + isMobileOnly + '&language=' + this.props.language)
        this.setState({teamcomparisonList: tcdic});
    }
  }

  handleStatChange(event){
    const newvalue = event.target.value
    if (this.state.selectedstat !== newvalue){
      this.setState(currentState => {
        return {
        ... currentState,
        selectedstat: newvalue,
        }
      });
    }
  }

  render() {
    const nostatmessage = createnostatMessage(this.props.language)
    if (!isEmpty(this.state.teamcomparisonList)){
      // get chart to be shown
      const chart = this.state.teamcomparisonList[this.state.selectedstat]
      return (
        <React.Fragment>
          <Selector stats={this.state.teamcomparisonList}  onChange={this.handleStatChange} value={this.state.selectedstat} />
          <Chart options={chart} language={this.props.language} />
        </React.Fragment>
      )
    }else{
      return (
          <div className="w3-padding-16 w3-center">{nostatmessage}</div>
      )
    }
  }
}
