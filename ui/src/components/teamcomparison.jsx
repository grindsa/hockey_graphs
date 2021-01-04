import React, {useState, useEffect} from 'react';
import { isMobileOnly } from 'react-device-detect';
import { Chart } from './teamcomparison/chart';
import { Selector } from './teamcomparison/selector';
// import { checkTcUpdate }  from './teamcomparison/teamcomparisonstateservice.js';
import { asyncGET, isEmpty } from './sharedfunctions.js';
import { createnostatMessage } from './localization.js';

export const TeamComparison = (props) => {
  // team-comparison
  const [teamcomparisonList, setTeamcomparisonList] = useState([])
  const [selectedstat, setSelectedstat] = useState(0)

  const handleStatChange = (event) => {
    const newValue = event.target.value
    if (selectedstat !== newValue){
      setSelectedstat(newValue)
    }
  }

  useEffect(() => {
    if (props.teamcomparison && props.season) {
      // get team comparison - run an async function inside useeffects...
      const tc_get = async () => {
        const tcdic = await asyncGET(props.teamcomparison + '?season=' + props.season + '&mobile=' + isMobileOnly + '&language=' + props.language)
        if (!isEmpty(tcdic)){
          setTeamcomparisonList(tcdic);
        }
      }
      tc_get()
    }
  }, [props.teamcomparison, props.season, props.language])

  const nostatmessage = createnostatMessage(props.language)
  if (!isEmpty(teamcomparisonList)){
    // get chart to be shown
    const chart = teamcomparisonList[selectedstat]
    return (
      <React.Fragment>
        <Selector stats={teamcomparisonList}  onChange={handleStatChange} value={selectedstat} />
        <Chart options={chart} language={props.language} />
      </React.Fragment>
    )
  }else{
    return (
        <div className="w3-padding-16 w3-center">{nostatmessage}</div>
    )
  }
}
