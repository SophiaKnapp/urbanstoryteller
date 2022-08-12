import React, {useRef, useEffect, useState} from 'react';
import '../../App.css';
import Card from '../UIElements/Card';
import * as d3 from "d3";
import WordCloud from 'react-d3-cloud';
import { scaleOrdinal } from 'd3-scale';

import { schemeCategory10 } from 'd3-scale-chromatic';
import {Colors} from "../../assets/colors";



// https://observablehq.com/@d3/bubble-chart

const WordCloudBox = ({selectedId, selectedHashtags}) => {

    const d3Chart = useRef();

    const [data, setData] = useState([]);
    const [width, setWidth] = useState(0);
    const [height, setHeight] = useState(0);

    const pickHighest = (obj, num = 1) => {
        const requiredObj = {};
        if(num > Object.keys(obj).length){
            return false;
        };
        Object.keys(obj).sort((a, b) => obj[b] - obj[a]).forEach((key, ind) =>
        {
            if(ind < num && ind !==0){
                requiredObj[key] = obj[key];
            }
        });
        return requiredObj;
    };



    useEffect(() => {

        if (selectedId !== undefined) {
            const path = process.env.PUBLIC_URL + '/data/hashtags_top/' + selectedId + '.json';
            // const path = process.env.PUBLIC_URL + '/data/example_frequency.json';

            d3.json(path).then(data => {
                console.log(data);
                setData(data);
                const mostFrequent = pickHighest(data, 30);
                console.log(mostFrequent);

            })
            setWidth(parseInt(d3.select('#wordclouddiv').style('width')));
            setHeight(parseInt(d3.select('#wordclouddiv').style('height')));
        }
    },
    [selectedId]);


    const schemeCategory10ScaleOrdinal = scaleOrdinal(schemeCategory10);
    return (

        <Card title={"Most popular hashtags"} description={""}>
            <div id="wordclouddiv" className="sider-card-wordcloud">

                <WordCloud
                    data={data}
                    width={width}
                    height={height}
                    font="sans-serif"
                    // fontSize={(word) => Math.log2(word.rank) * 5}

                    fontSize={(word) =>word.opacity *60}

                    spiral="rectangular"
                    rotate={(word) => 0}
                    padding={3}
                    // random={Math.random}
                    // fill={(d, i) => schemeCategory10ScaleOrdinal(d.opacity)}

                    fill={(d, i) => Colors.TURQUOISE}
                    onWordClick={(event, d) => {
                        console.log(`onWordClick: ${d.text}`);
                    }}
                    onWordMouseOver={(event, d) => {
                        console.log(`onWordMouseOver: ${d.text}`);
                    }}
                    onWordMouseOut={(event, d) => {
                        console.log(`onWordMouseOut: ${d.text}`);
                    }}
                />,
            </div>
        </Card>
    );
}
export default WordCloudBox;