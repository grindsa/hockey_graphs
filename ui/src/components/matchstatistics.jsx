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
        <h1>props: {this.props.match}</h1>
      </React.Fragment>
    );
  }
}
