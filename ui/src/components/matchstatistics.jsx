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
      <div className="w3-container w3-padding-small scolor w3-center">
        <h1>props: {this.props.match} <i className="w3-margin-left w3-xxlarge fa fa-arrow-circle-o-left" onClick={() => this.props.reset()} /></h1>
      </div>
      </React.Fragment>
    );
  }
}
