import React from 'react';
import { checkTcUpdate }  from './teamcomparison/teamcomparisonstateservice.js';
import { asyncGET } from './sharedfunctions.js';
import { createnostatMessage } from './localization.js';

export class TeamComparison extends React.Component {

  constructor(props) {
    super(props);
    this.state = {
      teamcomparisondic: [],
      selectedStat: null,
    };
  }

  async componentDidMount(){
    if (this.props.teamcomparison && this.props.season) {
      // get team comparison
      const matchdaydic = await asyncGET(this.props.teamcomparison + '?season=' + this.props.season)
      this.setState({teamcomparisondic: matchdaydic});
    }
  }

  async componentDidUpdate(prevProps) {
    /* we get the url to fectch as props and monitor it here */
    const tcupdate = checkTcUpdate(this.props.teamcomparison, prevProps.teamcomparison, this.props.season, prevProps.season)
    if (tcupdate){
        // get team comparison
        const tcdic = await asyncGET(this.props.teamcomparison + '?season=' + this.props.season)
        this.setState({teamcomparisondic: tcdic});
    }
  }

  render() {
    const nostatmessage = createnostatMessage(this.props.language)
    // <div className="w3-padding-16 w3-center">{nostatmessage}</div>
    return (
      <React.Fragment>
        <div className="w3-padding-16 w3-center">{nostatmessage}</div>
      </React.Fragment>
    )
  }
}
