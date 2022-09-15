import React, {useEffect, useState} from 'react';
import '../../App.css';
import LeafletMap from "./LeafletMap";
import * as d3 from "d3";
import {MapState} from "../../App";

const Map = ({setSelectedId, selectedId, potatoes, countsPerQuarter, showRelative, max, mapState})=>{

    const [potatoesWithOpacity, setPotatoesWithOpacity ] = useState(potatoes);

    const opacityLog = d3.scaleLinear()
        .domain([0,
            max[showRelative && mapState === MapState.hashtags ? 'relative' : 'absoluteMap']])
        .range([0.05, 1])

    useEffect(() => {
        const attribute = showRelative && mapState === MapState.hashtags ? 'relativeAmount' : 'count';
        let newPotatoes = [];
        const quarterCounts = {}

        Object.keys(countsPerQuarter).map((id) => {
            quarterCounts[id] = countsPerQuarter[id][attribute];
        })

        for (let i = 0; i < potatoes.length; i++) {
            let opacity = 0;
            if (max !== 0 && countsPerQuarter[potatoes[i].id] !== undefined) {
                opacity = opacityLog(quarterCounts[potatoes[i].id]);
            }
            const potato = potatoes[i];
            potato.properties.opacity = opacity;
            newPotatoes.push(potato);
        }
        setPotatoesWithOpacity(newPotatoes);
    }, [showRelative, max])


    return (
        <LeafletMap selectedId={selectedId} setSelectedId={setSelectedId} potatoesWithOpacity={potatoesWithOpacity} mapState={mapState}/>
    )

}
export default Map;