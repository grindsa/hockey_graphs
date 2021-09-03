import React, {useState, useEffect} from 'react';
import PropTypes from "prop-types";
import { isMobileOnly } from 'react-device-detect';
import { ReactSearchAutocomplete } from 'react-search-autocomplete'

export const Searchbar = (props) => {
  return (
    <div className="w3-center my-padding-4">
      <ReactSearchAutocomplete
        items={props.items}
        onSelect={props.onselect}
        autoFocus
        styling={{borderRadius: "1px",
                  boxShadow: "rgba(32, 33, 36, 0.28) 0px 0px 0px 0px",
                  backgroundColor: "#f1f2f3",
                  fontSize: "12px",
                  }}
      />
    </div>
  )
}
