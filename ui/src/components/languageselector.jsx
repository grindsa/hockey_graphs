import React from 'react';

export class LanguageSelector extends React.Component {

  constructor(props) {
    super(props);
  }

  render() {
    return (
      <div className="w3-dropdown-hover w3-right">
        <button onClick={() => this.props.onClick()} className ="w3-button">
          <span className="w3-tag w3-round w3-border pcolor">{this.props.langValue}</span>
        </button>
      </div>
    );
  }
}
