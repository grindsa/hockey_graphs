import React from 'react';

export const LanguageSelector = ({onClick, langValue}) => {
  return (
    <div className="w3-dropdown-hover w3-right w3-margin-top w3-margin-right">
      <div onClick={() => onClick()} className ="pcolor">
        <span className="w3-tag w3-round w3-border pcolor">{langValue}</span>
      </div>
    </div>
  );
}
