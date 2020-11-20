import React from 'react';

export class LanguageSelector extends React.Component {

  constructor(props) {
    super(props);
  }

  render() {
    return (
      <div className="w3-dropdown-hover w3-right w3-margin-top w3-margin-right">
        <div onClick={() => this.props.onClick()} className ="pcolor">
          <span className="w3-tag w3-round w3-border pcolor">{this.props.langValue}</span>
        </div>
      </div>
    );
  }
}
