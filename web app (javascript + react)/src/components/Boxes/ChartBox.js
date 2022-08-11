import React, {useRef, useEffect} from 'react';
import '../../App.css';
import Card from '../UIElements/Card';
import * as d3 from "d3";
import {Col} from "antd";
import {IGEmbed} from "react-ig-embed";

// https://observablehq.com/@d3/bubble-chart

const ChartBox = ({selectedId, selectedHashtags}) => {

    const d3Chart = useRef();

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

    const margin = 0;
    const marginTop = margin;
    const marginLeft = margin;
    const marginRight = margin;
    const marginBottom = margin;
    const padding = 3;

    const color = '#6ccfeb';
    const fill = "#ccc";

    const stroke = 1;
    const strokeWidth = 1;
    const fillOpacity = 0.7;


    useEffect(() => {

        if (selectedId !== undefined) {
            const path = process.env.PUBLIC_URL + '/data/hashtag_frequency_json/' + selectedId + '.json';

            d3.json(path).then(data => {
                const mostFrequent = pickHighest(data.count, 20);
                console.log(mostFrequent);

                d3.select(d3Chart.current)
                    .selectAll('a')
                    .remove();
                d3.select(d3Chart.current).selectAll('tspan')
                    .remove();


                const svg = d3.select(d3Chart.current);
                const width = parseInt(d3.select('#hashtagschart').style('width'));
                console.log(width);
                const height = width;

                const L = Object.keys(mostFrequent);
                const V = Object.values(mostFrequent);
                const I = d3.range(V.length).filter(i => V[i] > 0);
                const T = V;

                const root = d3.pack()
                    .size([width - marginLeft - marginRight, height - marginTop - marginBottom])
                    .padding(padding)
                    (d3.hierarchy({children: I})
                        .sum(i => V[i]));

                svg.attr("width", width)
                    .attr("height", width)
                    .attr("viewBox", [-marginLeft, -marginTop, width, height])
                    // .attr("style", "max-width: 100%; height: auto; height: intrinsic; background-color: blue;")
                    .attr("style", "max-width: 100%; height: auto; height: intrinsic;")
                    .attr("fill", "currentColor")
                    .attr("font-size", 10)
                    .attr("font-family", "sans-serif")
                    .attr("text-anchor", "middle");

                const leaf = svg.selectAll("a")
                    .data(root.leaves())
                    .join("a")
                    // .attr("xlink:href", link == null ? null : (d, i) => link(D[d.data], i, data))
                    // .attr("target", link == null ? null : linkTarget)
                    .attr("xlink:href", (d, i) => console.log(d))
                    // .attr("target", linkTarget)
                    .attr("transform", d => `translate(${d.x},${d.y})`);


                leaf.append("circle")
                    .attr("stroke", stroke)
                    .attr("stroke-width", strokeWidth)
                    // .attr("stroke-opacity", strokeOpacity)
                    .attr("fill", fill)
                    .attr("fill-opacity", fillOpacity)
                    .attr("r", d => d.r);

                if (T) leaf.append("title")
                    .text(d => T[d.data]);

                if (L) {
                    // A unique identifier for clip paths (to avoid conflicts).
                    const uid = `O-${Math.random().toString(16).slice(2)}`;

                    leaf.append("clipPath")
                        .attr("id", d => `${uid}-clip-${d.data}`)
                        .append("circle")
                        .attr("r", d => d.r);

                    leaf.append("text")
                        // .attr("clip-path", d => `url(${new URL(`#${uid}-clip-${d.data}`, location)})`)
                        .selectAll("tspan")
                        .data(d => `${'#' + L[d.data]}`.split(/\n/g))
                        .join("tspan")
                            .attr("x", 0)
                            .attr("y", (d, i, D) => `${i - D.length / 2 + 0.85}em`)
                            .attr("fill-opacity", (d, i, D) => i === D.length - 1 ? 0.7 : null)
                            .text(d => d);
                }
            })
        }
    },
    [selectedId]);
    return (
        <Card title={"Most popular hashtags"} description={""}>
            <div id="hashtagschart">
                <svg ref={d3Chart}>
                </svg>
            </div>
            {/*<div ref="myDiv"></div>*/}
        </Card>
    );
}
export default ChartBox;