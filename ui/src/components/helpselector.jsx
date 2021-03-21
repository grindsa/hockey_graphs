import React from 'react';
import PropTypes from "prop-types";

export const HelpSelector = (props) => {
  return (
      <div className = "pcolor w3-margin-top w3-margin-right w3-right w3-dropdown-hover">
        <span className="w3-round pcolor">?</span>
        <div className="w3-dropdown-content w3-bar-block w3-border helpselector">
          <a href="/dsgvo" className="w3-button pcolor"><i className="fa fa-user-shield" /></a>
          <a href="https://github.com/grindsa/hockey_graphs " className="w3-button pcolor"><i className="fab fa-github" /></a>
        </div>
      </div>
  );
}
