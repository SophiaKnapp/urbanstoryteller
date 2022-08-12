import React, {useEffect, useState} from 'react';
import '../../App.css';
import LeafletMap from "./LeafletMap";
import posts_users_stories from '../../assets/posts_users_stories.json';

import * as d3 from "d3";

const Map = ({setSelectedId, selectedId, potatoes, countsPerQuarter, showRelative, max, mapState, mapEvents})=>{

    const [potatoesWithOpacity, setPotatoesWithOpacity ] = useState(potatoes);


    // const color = d3.scaleLinear()
    //     .domain([0, 5])
    //     .range(["hsl(152,80%,80%)", "hsl(228,30%,40%)"])
    //     .interpolate(d3.interpolateHcl)

    const opacityLog = d3.scaleLinear()
        .domain([0,
            max[showRelative ? 'relative' : 'absoluteMap']])
        .range([0.05, 1])
        // .interpolate(d3.interpolateHcl)


    useEffect(() => {
        console.log("updating map...");

        const attribute = showRelative ? 'relativeAmount' : 'count';
        // const max = getMax(countsPerQuarter, attribute);
        let newPotatoes = [];

        // const countsLog = countsPerQuarter[potatoes[i].id][showRelative ? 'relativeAmount' : 'count']

        const quarterCounts = {}

        Object.keys(countsPerQuarter).map((id) => {
            // if (showRelative) {
            quarterCounts[id] = countsPerQuarter[id][attribute];
            // } else {
            //     quarterCounts[id] = Math.log(countsPerQuarter[id][attribute]/10);
            // }
        })

        for (let i = 0; i < potatoes.length; i++) {
            let opacity = 0;
            if (max !== 0 && countsPerQuarter[potatoes[i].id] !== undefined) {
                // opacity = opacityLog(countsPerQuarter[potatoes[i].id][showRelative ? 'relativeAmount' : 'count']);
                opacity = opacityLog(quarterCounts[potatoes[i].id]);
                // console.log(opacity);
            }
            const potato = potatoes[i];
            potato.properties.opacity = opacity;
            newPotatoes.push(potato);
        }
        setPotatoesWithOpacity(newPotatoes);
    }, [showRelative, max])

    // function getMax(obj, key)
    // {
    //     const values = Object.keys(obj).map(id => obj[id][key]);
    //     const maxValue = Math.max(...values);
    //     return maxValue;
    // }

    //
    function onMapClick() {
        // TODO: if clicked outside of geojson
       // if (selectedId !== undefined) {
       //     setSelectedId(undefined)
       // }
    }
    //
    //
    //     for (let i = 0; i < potatoes.length; i++) {
    //         //         if (showRelative) {
    //         //             const max = getMax(quarterCounts, 'relativeAmount');
    //         //
    //         //             potatoes[i].properties.opacity = quarterCounts
    //         //             // SELECT REALTIVE AMOUNT
    //         //         } else {
    //         //             const max = getMax(quarterCounts, 'userCount');
    //         //             // SELECT USER COUNT
    //         //         }
    //         //
    //         //         potatoes[i].properties.opacity = quarterOpacities[potatoes[i].id];
    //         //         potatoes[i].properties.userCount = quarterCounts[potatoes[i].id];
    //         //
    //
    //         const value = showRelative ? quarterCounts[]
    //
    //         potatoes[i].properties.opacity = 0.5;
    //     }
    //
    //     } else {
    //
    //         console.log("quarterOpacities");
    //         const quarterOpacities = normalizeValues(quarterCounts);
    //
    //
    //
    //         console.log(quarterOpacities);
    //
    //
    //
    //
    //
    //
    // }

    return (
        <LeafletMap selectedId={selectedId} setSelectedId={setSelectedId} potatoesWithOpacity={potatoesWithOpacity} onMapClick={onMapClick} mapState={mapState}/>
    )

}
export default Map;