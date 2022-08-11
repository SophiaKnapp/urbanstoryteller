import React, {useRef, useEffect, useState} from 'react';
import '../../App.css';
import Card from '../UIElements/Card';
import * as d3 from "d3";
import WordCloud from 'react-d3-cloud';
import { scaleOrdinal } from 'd3-scale';

import { schemeCategory10 } from 'd3-scale-chromatic';
import {Colors} from "../../assets/colors";
// import {Legend, Swatches} from "@d3/color-legend"
import getCount from "../../assets/hashtag_frequencies";

// https://observablehq.com/@d3/stacked-bar-chart
// https://observablehq.com/@d3/bubble-chart

const HistogramBox = ({quarterCounts, selectedHashtags}) => {

    // data.sort(function(a, b) {
    //     return a.userCount - b.userCount;
    // });

    console.log(quarterCounts);

    let data = [];

    // Object.keys(values2).map(function(key, index) {
    //     values3.push({"quarter": key, "userCount": values2[key].userCount})
    // });
    //




    const x = (d) => {
        return showRelative ? d.relativeAmount : d.userCount;
        }; // given d in data, returns the (ordinal) x-value

    const y = (d,i) => {
        return d.quarter;
    }; // given d in data, returns the (ordinal) x-value


    const z = (d) => {
        // return d['cluster'];
        return 0;
    }; // given d in data, returns the (ordinal) x-value

    let title = x; // given d in data, returns the title text
    const marginTop = 30; // top margin, in pixels
    const marginRight = 10; // right margin, in pixels
    const marginBottom = 30; // bottom margin, in pixels
    const marginLeft = 100; // left margin, in pixels

    var width = 600;
    var height = 500;


    const xType = d3.scaleLinear; // type of x-scale
    // let xDomain = [0,500];
    let xDomain = undefined;
    const xRange = [marginLeft, width - marginRight]; // [left, right]
    const yPadding = 0.1; // amount of y-range to reserve to separate bars
    const offset = d3.stackOffsetDiverging; // stack offset method
    // const order = d3.stackOrderNone; // stack order method

    const order = d3.stackOrderDescending;

    const colors = d3.schemeTableau10;

    const d3Chart = useRef();

    let yDomain = undefined;
    let zDomain = [0];
    let yRange = undefined;

    let xLabel = undefined;
    let xFormat = undefined;

    const getColor = (i) => {
        // switch (i) {
        //     case 0:
        //         return Colors.instagramPink;
        //     case 1:
        //         return Colors.TURQUOISE;
        //     case 2:
        //         return Colors.instagramYellow;
        // }
        return Colors.TURQUOISE;
    }


    useEffect(() => {
        d3.selectAll("svg > *").remove();

        const X = d3.map(data, x);
        const Y = d3.map(data, y);
        const Z = d3.map(data, z);

        // Compute default y- and z-domains, and unique them.
        if (yDomain === undefined) yDomain = Y;
        if (zDomain === undefined) zDomain = Z;
        yDomain = new d3.InternSet(yDomain);
        zDomain = new d3.InternSet(zDomain);

        // Omit any data not present in the y- and z-domains.
        const I = d3.range(X.length).filter(i => yDomain.has(Y[i]) && zDomain.has(Z[i]));

        // If the height is not specified, derive it from the y-domain.
        if (height === undefined) height = yDomain.size * 25 + marginTop + marginBottom;
        if (yRange === undefined) yRange = [height - marginBottom, marginTop];
        //
        // Compute the default x-domain. Note: diverging stacks can be negative.
        //
        // Compute a nested array of series where each series is [[x1, x2], [x1, x2],
        // [x1, x2], …] representing the x-extent of each stacked rect. In addition,
        // each tuple has an i (index) property so that we can refer back to the
        // original data point (data[i]). This code assumes that there is only one
        // data point for a given unique y- and z-value.

        const series = d3.stack()
            .keys(zDomain)
            .value(([, I], z) => X[I.get(z)])
            .order(order)
            .offset(offset)
            (d3.rollup(I, ([i]) => i, i => Y[i], i => Z[i]))
            .map(s => s.map(d => Object.assign(d, {i: d.data[1].get(s.key)})));

        console.log("series");
        console.log(series);


        // Compute the default x-domain. Note: diverging stacks can be negative.
        if (xDomain === undefined) xDomain = d3.extent(series.flat(2));



        // Construct scales, axes, and formats.
        const xScale = xType(xDomain, xRange);
        const yScale = d3.scaleBand(yDomain, yRange).paddingInner(yPadding);
        const color = d3.scaleOrdinal(zDomain, colors);
        const xAxis = d3.axisTop(xScale).ticks(width / 80, xFormat);
        const yAxis = d3.axisLeft(yScale).tickSizeOuter(0);

        // Compute titles.
        // if (title === undefined) {
        //     const formatValue = xScale.tickFormat(100, xFormat);
        //     title = i => `${Y[i]}\n${Z[i]}\n${formatValue(X[i])}`;
        // } else {
        //     const O = d3.map(data, d => d);
        //     const T = title;
        //     title = i => T(O[i], i, data);
        // }

        const svg = d3.select(d3Chart.current);

        svg.attr("width", width)
            .attr("height", height)
            .attr("viewBox", [0, 0, width, height])
            .attr("style", "max-width: 100%; height: auto; height: intrinsic;");

        svg.append("g")
            .attr("transform", `translate(0,${marginTop})`)
            .call(xAxis)
            .call(g => g.select(".domain").remove())
            .call(g => g.selectAll(".tick line").clone()
                .attr("y2", height - marginTop - marginBottom)
                .attr("stroke-opacity", 0.1))
            .call(g => g.append("text")
                .attr("x", width - marginRight)
                .attr("y", -22)
                .attr("fill", "currentColor")
                .attr("text-anchor", "end")
                .text(xLabel));


        const bar = svg.append("g")
            .selectAll("g")
            .data(series)
            .join("g")
                .attr("fill", ([{i}]) => getColor(Z[i]))
            // .attr("fill", (i) => getColor(i))
            .selectAll("rect")
            .data(d => d)
            .join("rect")
            .attr("x", ([x1, x2]) => Math.min(xScale(x1), xScale(x2)))
            .attr("y", ({i}) => yScale(Y[i]))
            .attr("width", ([x1, x2]) => Math.abs(xScale(x1) - xScale(x2)))
            .attr("height", yScale.bandwidth());

        // if (title) bar.append("title")
        //     .text(({i}) => title(i));

        svg.append("g")
            .attr("transform", `translate(${xScale(0)},0)`)
            .call(yAxis);


    }, [data]);

    return (

        <Card title={"Most popular hashtags"} description={""}>
            <div id="histogrambox" className="sider-card-clusters">
                <svg ref={d3Chart}>
                </svg>
            </div>
        </Card>
    );
}
export default HistogramBox;