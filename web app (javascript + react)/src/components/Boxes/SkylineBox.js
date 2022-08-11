import React, {useRef, useEffect, useState} from 'react';
import '../../App.css';
import Card from '../UIElements/Card';
import * as d3 from "d3";
import WordCloud from 'react-d3-cloud';
import { scaleOrdinal } from 'd3-scale';

import { schemeCategory10 } from 'd3-scale-chromatic';
import {Colors} from "../../assets/colors";
import {Sizes} from "../../assets/constants";

const SkylineBox = ({countsPerQuarter, max, selectedId, setSelectedId, hoverId, setHoverId}) => {
    const d3Chart = useRef();
    const svg = d3.select(d3Chart.current);
    const width = Sizes.siderWidth;
    const [height, setHeight] = useState(0);

    const [data, setData] = useState([]);

    const margin = 0;
    const marginTop = 20;
    const marginBottom = 30;
    const marginLeft = 35;
    const marginRight = 20;
    const yPadding = 0.1;
    const fontSize = 10;

    svg.attr("width", width)
        .attr("height", height)
        .attr("viewBox", [0, 0, width, height])
        // .attr("style", "max-width: 100%; height: auto; height: intrinsic;");

    const bars = svg.selectAll('.bar')
        .data(data, (d) => d.quarter)
        .join('rect')
        .attr("class", "bar")
        .attr("fill", 'none')
        .attr("x", marginLeft)
        .attr("fill", (d) => d.quarter === selectedId ? Colors.district : Colors.hashtags)
        .attr("stroke", (d) => d.quarter === selectedId ? Colors.district : Colors.hashtags)
        .attr("stroke-width", '2px')
        .attr("fill-opacity", 0.01)
        .on("mouseover", function() { d3.select(this).attr("fill-opacity", 0.1); })
        .on("mouseout", function() { d3.select(this).attr("fill-opacity", 0.01); })
        .on("click", (event, d) => setSelectedId(d.quarter));
        // .attr("height",  yScale.bandwidth())


    const labels = svg.selectAll('.label-graph')
        .data(data, (d) => d.quarter)
        .join('text')
        .attr("class", "label-graph")
        // .style("font", `${fontSize}px HelveticaNeue-Light`)
        // .style("display", (d) => bubbleLayout === BubbleLayout.CLUSTER && selectedCluster !== d.cluster ? 'none' : 'inline')
        .attr("pointer-events", "none")
        .text((d) => `#${d.quarter}`)
        .attr("text-anchor", "end")
        // .attr("x", marginLeft)
        // .attr("y", height-marginBottom)


    svg.append("text")
        .attr("class", "label-axis")
        .attr("text-anchor", "end")
        .attr("x", width-marginRight)
        .attr("y",height+ 5)
        .text('n users');

    svg.append("text")
        .attr("class", "label-axis")
        .attr("text-anchor", "start")
        .attr("x", 5)
        .attr("y",0)
        .text('% of users');

    useEffect(() => {
        // setWidth(parseInt(d3.select('#skylinechart').style('width'))); // INFLUENCES FONT SIZE, not where the bubbles go
        setHeight(parseInt(d3.select('#skylinechart').style('height')));
        // setHeight(500);
        const dataArray = [];

        console.log('updating ABSOLUTE RELATIVE')


        Object.keys(countsPerQuarter)
            .map(id => dataArray.push({
                'quarter': id,
                'count': countsPerQuarter[id].count,
                'relativeAmount': countsPerQuarter[id].relativeAmount,
            }));


        console.log(dataArray);
        dataArray.sort(function(a, b) {
            return b.relativeAmount * b.count - a.relativeAmount * a.count;
        });

        setData(dataArray.slice(0,10));

        bars
            .attr("y", height-marginBottom)
            .attr("width", 0)
            .attr("height", 0);


    }, [max])
    // TODO: nur max genug?

    useEffect(() => {
        d3.selectAll("#skylinechart > svg > g").remove();
        const yDomain = [0, max['relative']];
        const yRange = [height - marginBottom, marginTop];
        const yScale = d3.scaleLinear(yDomain, yRange);
        const yAxis = d3.axisLeft(yScale).tickFormat(d => {
                return Math.floor(d *100) + "%";
        });;
        const xDomain = [0,max['absolute']];

        if (xDomain[1] !== 0) {
            const xRange = [marginLeft, width - marginRight];
            const xScale = d3.scaleLinear(xDomain, xRange);
            const xAxis = d3.axisBottom(xScale);
                // .ticks(width / 80);

            svg.append("g")
                .attr("transform", `translate(0,${height-marginBottom})`)
                .call(xAxis)

            bars.transition()
                .duration(600)
                .attr("width", d => xScale(d.count) - marginLeft)
                .attr("y", d => yScale(d.relativeAmount))
                .attr("height", d => height - marginBottom - yScale(d.relativeAmount));

            labels
                .attr("transform", (d) => `translate(${0},${height-marginBottom})`)

            labels.transition()
                .duration(600)
                .attr("transform", (d) => `translate(${xScale(d.count)},${yScale(d.relativeAmount) - 5})`)

        } else {
            bars.transition().duration(600)
                .attr("y",height-marginBottom)
                .attr("width", 0)
                .attr("height", 0);


        }
        // TODO: refactor (könnte draußen sein)
        svg.append("g")
            .attr("transform", `translate(${marginLeft},0)`)
            .call(yAxis);
    }, [data]);

    // classname does not exist
    return (

                <div id="skylinechart" className="sider-card">
                    <svg ref={d3Chart} className="svg-class">
                    </svg>
                </div>

    );
}
export default SkylineBox;