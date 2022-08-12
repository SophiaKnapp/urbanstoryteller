import React, {useRef, useEffect, useState} from 'react';
import '../../App.css';
import * as d3 from "d3";
import {Colors} from "../../assets/colors";
import posts_users_stories from '../../assets/posts_users_stories.json';
import {Sizes} from "../../assets/constants";

const HistogramBox = ({setSelectedId}) => {
    const d3Chart = useRef();
    const svg = d3.select(d3Chart.current);

    const width = Sizes.siderWidth;
    const [height, setHeight] = useState(0);

    useEffect(() => {
        setHeight(parseInt(d3.select('#histogramchart').style('height')));
    }, [])

    const marginTop = 25;
    const marginBottom = 10;
    const marginLeft = 80;
    const marginRight = 20;
    const yPadding = 0.1;

    svg.append("text")
        .attr("class", "label-axis")
        .attr("text-anchor", "end")
        .attr("x", width-marginRight)
        .attr("y",0)
        .text('Users talking about this')

    const districtsSorted = posts_users_stories.sort(function (a, b) {
        return a.users - b.users;
    })


    let Y = districtsSorted.map((potato) => potato.quarter)

    const yDomain = new d3.InternSet(Y);
    const yRange = [height - marginBottom, marginTop];
    const yScale = d3.scaleBand(yDomain, yRange).paddingInner(yPadding);
    const yAxis = d3.axisLeft(yScale).tickSizeOuter(0).tickFormat(d => '#' + d);


    const X = districtsSorted.map((d) => d.users);
    const xDomain = [0,d3.max(X)];
    const xRange = [marginLeft, width - marginRight];
    const xScale = d3.scaleLinear(xDomain, xRange);
    const xAxis = d3.axisTop(xScale)
        .ticks(width / 80)
        .tickFormat(d =>  d);


    svg.attr("width", width)
        .attr("height", height)
        .attr("viewBox", [0, 0, width, height])

    const bars = svg.selectAll('.bar')
        .data(districtsSorted)
        .join('rect')
        .attr("class", "bar")
        .attr("fill", Colors.posts)
        .attr("x", marginLeft)
        .attr("y", d => yScale(d.quarter))
        .attr("height",  yScale.bandwidth())
        .attr("width",  (d) => xScale(d.users) -marginLeft)
        .on("mouseover", function() { d3.select(this).attr("fill", Colors.district); })
        .on("mouseout", function() { d3.select(this).attr("fill", Colors.posts); })
        .on("click", (event, d) => setSelectedId(d.quarter));

    d3.selectAll("#histogramchart > svg > g").remove();

    svg.append("g")
        .attr("transform", `translate(0,${marginTop})`)
        .call(xAxis)
        .call(g => g.select(".domain").remove())
        .call(g => g.selectAll(".tick line").clone()
            .attr("y2", height - marginTop - marginBottom)
            .attr("stroke-opacity", 0.1))

    svg.append("g")
        .attr("transform", `translate(${marginLeft},0)`)
        .call(yAxis);

    return (
            <div className="sider-card" id="histogramchart">
                <svg ref={d3Chart} className="svg-class">
                </svg>
            </div>
    );
}
export default HistogramBox;