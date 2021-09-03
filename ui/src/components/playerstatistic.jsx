import React, {useState, useEffect} from 'react';
import { isMobileOnly } from 'react-device-detect';
import { Searchbar } from './playerstatistics/searchbar';
import { createnostatMessage } from './localization.js';
import { asyncGET, asyncGETPaging, isEmpty } from './sharedfunctions.js';
import { navigate } from "hookrouter";

export const Playerstatistic = (props) => {
  // console.log(props)
  // team-comparison
  const [playerstatList, setPlayerstatList] = useState([])
  const [selectedstat, setSelectedstat] = useState(0)

  const handleOnSelect = (item) => {
    // the item selected
    console.log(item)
  }

  useEffect(() => {
    if (props.players && props.season) {
      // get team comparison - run an async function inside useeffects...
      const plist_get = async () => {
        // const plist = await asyncGET(props.players + '?season=' + props.season + '&mobile=' + isMobileOnly)
        const plist = await asyncGETPaging(props.players + '?season=' + props.season + '&mobile=' + isMobileOnly, 'next', 'results')
        if (!isEmpty(plist)){
          setPlayerstatList(plist);
        }
      }
      plist_get()
    }
  }, [props.playerstatistic, props.season, props.language])

  useEffect(() => {
      if (props.stat){
        setSelectedstat(props.stat-1)
      }
  }, [props.stat, props.players])

  const nostatmessage = createnostatMessage(props.language)
  if (!isEmpty(playerstatList)){
    // get chart to be shown
    const chart = playerstatList[selectedstat]
    return (
      <Searchbar items={playerstatList} onselect={handleOnSelect} />
    )
  }else{
    return (
        <div className="w3-padding-16 w3-center">{nostatmessage}</div>
    )
  }
}
