import React, {useState, useEffect} from 'react';
import { isMobileOnly } from 'react-device-detect';
import { Searchbar } from './playerstatistics/searchbar';
import { Selector } from './playerstatistics/selector';
import { Chart } from './playerstatistics/chart';
import { selectPlayerItem }  from './playerstatistics/playerstatisticstateservice.js';
import { createnostatMessage } from './localization.js';
import { asyncGET, asyncGETPaging, isEmpty } from './sharedfunctions.js';
import { navigate } from "hookrouter";

export const Playerstatistic = (props) => {
  // team-comparison
  const [playerList, setPlayerList] = useState([])
  const [selectedPlayer, setPlayer] = useState({})
  const [playerstatList, setPlayerstatList] = useState([])
  const [selectedstat, setSelectedstat] = useState(0)

  const handleStatChange = (event) => {
    const newValue = event.target.value
    if (selectedstat !== newValue){
      const linkValue =  parseInt(newValue) + 1
      navigate('/playerstatistics/' + props.season + '/' + selectedPlayer.id + '/' + linkValue)
    }
  }

  const pstat_get = async (player_id) => {
    const statlist = await asyncGET(props.playerstatistics + props.season + '/' + player_id + '?mobile=' + isMobileOnly  + '&language=' + props.language)
    if (!isEmpty(statlist)){
      setPlayerstatList(statlist);
    }
  }

  const handleOnSelect = (item) => {
    // the item selected
    setPlayer(item)
    pstat_get(item.id)
    navigate('/playerstatistics/' + props.season + '/' + item.id )
  }

  useEffect(() => {
    if (props.players && props.season) {
      // get playerstats - run an async function inside useeffects...
      const plist_get = async () => {
        const plist = await asyncGETPaging(props.players + '?season=' + props.season + '&mobile=' + isMobileOnly, 'next', 'results')
        if (!isEmpty(plist)){
          setPlayerList(plist);
        }
      }
      plist_get()
    }
  }, [props.players, props.season, props.language, props.player_id])

  useEffect(() => {
    if (props.season && props.player_id && !isEmpty(playerList)) {
      pstat_get(props.player_id)
      var item = selectPlayerItem(playerList, props.player_id)
      if(item){
        // player lookup was successfull
        setPlayer(item)
      }else{
        // fall back
        setPlayer({'id': props.player_id})
      }
    }
  }, [props.player_id, props.season, props.language, playerList])


  useEffect(() => {
    if (props.stat){
      setSelectedstat(props.stat-1)
    }
  }, [props.stat, props.players])

  const nostatmessage = createnostatMessage(props.language)
  if (!isEmpty(playerList)){
    // get chart to be shown
    const chart = playerstatList[selectedstat]
    return (
      <React.Fragment>
        <Searchbar items={playerList} onselect={handleOnSelect}  PlayerName={selectedPlayer.name}/>
        <div>{selectedPlayer.name}</div>
        <Selector stats={playerstatList}  onChange={handleStatChange} value={selectedstat} />
        <Chart options={chart} language={props.language} />
      </React.Fragment>
    )
  }else{
    return (
        <div className="w3-padding-16 w3-center">{nostatmessage}</div>
    )
  }
}
