import React from 'react';

export class MatchStatistics extends React.Component {
  constructor(props) {
    super(props);
    if (props.match){
      this.state = {
        match: props.match,
      };
    }
  }

  componentDidMount(){
    console.log('state', this.state.match)
  }

  render() {
    return (
      <React.Fragment>
      <MatchHeader match={this.props.match} reset={this.props.reset} />
      </React.Fragment>
    );
  }
}

export class MatchHeader extends React.Component {
  render() {
    return (
      <div className="w3-container w3-padding-small scolor w3-center">
        <h1>
          <span className="w3-padding-small pseudohead">{this.props.match.home_team_name}</span>
          <span className="w3-padding-small middle"><img src={this.props.match.home_team_logo} alt={this.props.match.home_team_shortcut} width="40px"/></span>
          <span className="w3-padding-small">{this.props.match.result}</span>
          <span className="w3-padding-small middle"><img src={this.props.match.visitor_team_logo} alt={this.props.match.visitor_team_logo} width="40px"/></span>
          <span className="w3-padding-small pseudohead">{this.props.match.visitor_team_name}</span>
          <span className="w3-padding-small"><i className="w3-margin-right w3-xxlarge fa fa-arrow-circle-o-left w3-right" onClick={() => this.props.reset()} /></span>
        </h1>
      </div>
    );
  }
}
