import React, {useRef, useEffect, useState} from 'react';
import '../../App.css';
import Card from '../UIElements/Card';
import * as d3 from "d3";
import {Col} from "antd";
import {IGEmbed} from "react-ig-embed";
import {Colors} from "../../assets/colors";

const ClustersBox = ({selectedId, selectedHashtags}) => {

    const d3Chart = useRef();

    const margin = 0;
    const marginTop = margin;
    const marginLeft = margin;
    const marginRight = margin;
    const marginBottom = margin;
    const padding = 3;

    const color = d3.scaleLinear()
        .domain([0, 5])
        .range(["hsl(152,80%,80%)", "hsl(228,30%,40%)"])
        .interpolate(d3.interpolateHcl)
    const fill = "#ccc";

    const stroke = 1;
    const strokeWidth = 1;
    const fillOpacity = 0.7;

    const [width, setWidth] = useState(0);
    const [height, setHeight] = useState(0);

    const factorFontSize = 0.8;
    const factorViewBox = 1.3;
    const factorZoom = 2.4;

    useEffect(() => {

        const getColor = (d) => {
            const color = selectedHashtags.includes(d.data.name) ? Colors.instagramPink : Colors.TURQUOISE;
            return color;

        }

        if (selectedId !== undefined) {
            const path = process.env.PUBLIC_URL + '/data/clusters/' + selectedId + '.json';
            // const path = process.env.PUBLIC_URL + '/data/example_cluster.json';

            setWidth(parseInt(d3.select('#clustersschart').style('width'))*factorFontSize); // INFLUENCES FONT SIZE, not where the bubbles go
            setHeight(parseInt(d3.select('#clustersschart').style('height'))*factorFontSize);

            d3.json(path).then(data => {

                const svg = d3.select(d3Chart.current);
                console.log(data);


                const root = d3.pack()
                    .size([width - marginLeft - marginRight, height - marginTop - marginBottom])
                    .padding(padding)
                    (d3.hierarchy(data)
                        .sum(d => d.count)
                        .sort((a, b) => b.count - a.count));

                //
                // const root = d3.pack()
                //     .size([width - marginLeft - marginRight, height - marginTop - marginBottom])
                //     .padding(padding)
                //     (d3.hierarchy({children: I})
                //         .sum(i => V[i]));

                let focus = root;
                let view;


                svg
                    .attr("viewBox", `-${width*factorViewBox / 2} -${height*factorViewBox / 2} ${width*factorViewBox} ${height*factorViewBox}`)

                    // .attr("viewBox", [-marginLeft, -marginTop, width, height])
                    // .attr("style", "max-width: 100%; height: auto; height: intrinsic; background-color: blue;")
                    // .attr("style", "max-width: 100%; height: auto; height: intrinsic; background-color: blue;")

                    .style("display", "block")
                    // .style("margin", "0 -14px")
                    .on("click", (event) => zoom(event, root));


                d3.select(d3Chart.current)
                    .selectAll('g')
                    .remove();
                // d3.select(d3Chart.current).selectAll('tspan')
                //     .remove();

                const node = svg.append("g")
                    .selectAll("circle")
                    .data(root.descendants().slice(1))
                    .join("circle")
                    .attr("fill", d => d.children ? "white" : getColor(d))
                    .attr("fill-opacity", d => d.children? 0 : d.data.opacity)
                    .attr("stroke", d => d.children ? Colors.TURQUOISE : 'white')
                    .attr("pointer-events", d => !d.children ? "none" : null)
                    .on("mouseover", function() { d3.select(this).attr("stroke", "#000"); })
                    .on("mouseout", function() { d3.select(this).attr("stroke", null); })
                    .on("click", (event, d) => focus !== d && (zoom(event, d), event.stopPropagation()));


                const label = svg.append("g")
                    .style("font", "10px sans-serif")
                    .attr("pointer-events", "none")
                    .attr("text-anchor", "middle")
                    .selectAll("text")
                    .data(root.descendants())
                    .join("text")
                    .style("fill-opacity", d => d.parent === root ? 1 : 0.5)
                    .style("display", d => d.parent === root ? "inline" : "none")
                    .text(d => d.data.name);
                zoomTo([root.x, root.y, root.r * 2]);

                function zoom(event, d) {
                    const focus0 = focus;

                    focus = d;

                    const transition = svg.transition()
                        .duration(event.altKey ? 7500 : 750)
                        .tween("zoom", d => {
                            const i = d3.interpolateZoom(view, [focus.x, focus.y, focus.r * factorZoom]);
                            return t => zoomTo(i(t));
                        });


                    label
                        .filter(function(d) { return d.parent === focus || this.style.display === "inline"; })
                        .transition(transition)
                        .style("fill-opacity", d => d.parent === focus ? 1 : 0)
                        .on("start", function(d) { if (d.parent === focus) this.style.display = "inline"; })
                        .on("end", function(d) { if (d.parent !== focus) this.style.display = "none"; });
                }


                function zoomTo(v) {
                    const k = width / v[2];
                    view = v;

                    label.attr("transform", d => `translate(${(d.x - v[0]) * k},${(d.y - v[1]) * k})`);
                    node.attr("transform", d => `translate(${(d.x - v[0]) * k},${(d.y - v[1]) * k})`);
                    node.attr("r", d => d.r * k);

                }
            })
        }
    },
    [selectedId, selectedHashtags]);
    return (
        <Card title={"Clusters"} description={""}>
            <div id="clustersschart" className="sider-card-clusters">
                <svg ref={d3Chart}>
                </svg>
            </div>
        </Card>
    );
}
export default ClustersBox;