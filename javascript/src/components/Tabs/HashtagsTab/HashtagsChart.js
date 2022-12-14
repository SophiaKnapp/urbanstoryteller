import React, {useRef, useEffect, useState} from 'react';
import '../../../App.css';
import * as d3 from "d3";
import {Colors} from "../../../assets/colors";
import {Sizes} from "../../../assets/constants";

const HashtagsChart = ({countsPerQuarter, max, selectedId, setSelectedId, selectedCluster, selectedHashtags}) => {
    const d3Chart = useRef();
    const svg = d3.select(d3Chart.current);
    const width = Sizes.siderWidth;
    const [height, setHeight] = useState(0);

    const [data, setData] = useState([]);

    const marginTop = 20;
    const marginBottom = 30;
    const marginLeft = 35;
    const marginRight = 20;

    svg.attr("width", width)
        .attr("height", height)
        .attr("viewBox", [0, 0, width, height])

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

    const labels = svg.selectAll('.label-graph')
        .data(data, (d) => d.quarter)
        .join('text')
        .attr("class", "label-graph")
        .attr("pointer-events", "none")
        .text((d) => `#${d.quarter}`)
        .attr("text-anchor", "end")


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
        setHeight(parseInt(d3.select('#skylinechart').style('height')));
        const dataArray = [];

        Object.keys(countsPerQuarter)
            .map(id => dataArray.push({
                'quarter': id,
                'count': countsPerQuarter[id].count,
                'relativeAmount': countsPerQuarter[id].relativeAmount,
            }));


        dataArray.sort(function(a, b) {
            return b.relativeAmount * b.count - a.relativeAmount * a.count;
        });

        setData(dataArray.slice(0,10));

        bars
            .attr("y", height-marginBottom)
            .attr("width", 0)
            .attr("height", 0);


    }, [max])

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
        svg.append("g")
            .attr("transform", `translate(${marginLeft},0)`)
            .call(yAxis);
    }, [data]);


    const getText = (selectedHashtags, selectedCluster) => {
        let text = 'The graph shows how many people who mention a district also mention ';


        if (selectedHashtags.length === 1) {
            text += '#' + selectedHashtags[0];
        } else if (selectedHashtags.length > 1) {
            text += '#';
            let exceptLast = selectedHashtags.slice(0, selectedHashtags.length - 1);
            let hashtagsString = exceptLast.join(', #');
            hashtagsString += ' or #' + selectedHashtags[selectedHashtags.length - 1];
            text += hashtagsString;
        }



        if (selectedCluster) {
            if (selectedHashtags.length > 0) {
                text+= ' or'
            } else {

            }
            text += ' hashtags related to story #' + selectedCluster.name;
        }

        return text;
    }

    return (

                <div id="skylinechart" className="sider-card">
                    <div>
                        <div>{getText(selectedHashtags, selectedCluster)}</div>
                    </div>
                    <svg ref={d3Chart} className="svg-class">
                    </svg>
                </div>

    );
}
export default HashtagsChart;