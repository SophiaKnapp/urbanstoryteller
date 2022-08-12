import React, {useRef, useEffect, useState} from 'react';
import '../../App.css';
import * as d3 from "d3";
import {Colors} from "../../assets/colors";
import {BubbleLayout} from "./ClustersBox";
import {Sizes} from "../../assets/constants";



const ClustersChart = ({selectedId, selectedHashtags, addHashtag, removeHashtag, bubbleLayout, selectedCluster, setSelectedCluster}) => {

    const d3Chart = useRef();

    const opacityScale = d3.scaleLinear()
        .domain([0,10])
        .range([0.05, 1])

    const legendHeight = 15;

    const width = Sizes.siderWidth;
    const [height, setHeight] = useState(0);

    const [data, setData] = useState([]);
    const [visibleBubbles, setVisibleBubbles] = useState([]);
    const [parents, setParents] = useState([]);
    const [focus, setFocus] = useState(undefined);
    const [prevFocus, setPrevFocus] = useState(undefined);

    const [animationDuration, setAnimationDuration] = useState(500); // TODO: not use when first loaded




    const rootView = [width/2, height/2, width];


    useEffect(() => {
        setHeight(parseInt(d3.select('#clusterschart').style('height')));
        console.log(`setting height to ${height}`);
    }, [])


    const margin = 15;
    const marginTop = 20;
    const marginLeft = 26;
    const marginRight = 0;
    const marginBottom = 0;
    const padding = 3;

    const nx = 5;
    const fontSize = 14;
    const fontSizeSmall = 10;
    const maxLetters = 13;

    const fontFamily = "'HelveticaNeue-Light', 'Helvetica Neue Light', 'Helvetica Neue', Helvetica, Arial, 'Lucida Grande', sans-serif";

    const xScale = d3.scaleBand()
        .domain([...Array(nx).keys()])
        .rangeRound([0,width-marginRight-marginLeft])
        .padding(0.1);

    const ny = Math.floor(height/(xScale.bandwidth() + 2 * fontSizeSmall));
    const yScale = d3.scaleBand()
        .domain([...Array(ny).keys()])
        .rangeRound([0,height-marginTop-marginBottom])
        .padding(0.1);

    const cutIfNeeded = (text) => {
        const result = text.length > maxLetters ? text.slice(0, maxLetters) + '...' : text;
        return `#${result}`
    }

    function getX(index) {
        return index % nx;
    }

    function getY(index) {
        return Math.floor(index/nx);
    }

    const svg = d3.select(d3Chart.current);

    svg
        .attr("viewBox", [-marginLeft, -marginTop, width, height])
        .style("display", "block")
        .on("click", (event) => {
            if (bubbleLayout === BubbleLayout.CLUSTER && selectedCluster !== undefined) {
                setFocus(undefined);
            }
        });

    const bubbles = svg.selectAll('.child')
        .data(visibleBubbles, (d) => d.hashtag)
        .join('circle')
        .attr("class", "child")
        .attr("fill", (d) => {
            if (selectedHashtags.length > 0) {
                return selectedHashtags.includes(d.hashtag) ? Colors.hashtags : Colors.district;
            } else {
                return Colors.district;
            }
        })
        .attr("fill-opacity", (d) => opacityScale(d.uniqueness))
        .attr("r", (d) => {
            return d.radius*xScale.bandwidth()/2;
        })
        .style("display", (d) => bubbleLayout === BubbleLayout.CLUSTER && selectedCluster !== undefined && selectedCluster.name !== d.cluster && focus ? 'none' : 'inline')
        .on("mouseover", function() { d3.select(this).attr("stroke", "#000"); })
        .on("mouseout", function() { d3.select(this).attr("stroke", null); })
        .on("click", (event, d) => {
            if (selectedHashtags.includes(d.hashtag)) {
                removeHashtag(d.hashtag);
            } else {
                addHashtag(d.hashtag);
            }
        });

    const labels =
        svg.selectAll(".nodelabel")
        .data(visibleBubbles, (d) => d.hashtag )
        .join("text")
            .attr("class", "nodelabel")
            .style("font", `${fontSize}px ${fontFamily}`)
            .style("text-anchor", "middle")
            .style("display", (d) => bubbleLayout === BubbleLayout.CLUSTER && ((selectedCluster && selectedCluster.name !== d.cluster && focus) || !selectedCluster) ? 'none' : 'inline')
            .text((d) => cutIfNeeded(d.hashtag));


    const labelsSmall =
        svg.selectAll(".nodelabelsmall")
            .data(visibleBubbles, (d) => d.hashtag)
            .join("text")
            .attr("class", "nodelabelsmall")
            .style("font", `${fontSizeSmall}px ${fontFamily}`)
            .style("text-anchor", "middle")
            .style("display", (d) => bubbleLayout === BubbleLayout.CLUSTER ? 'none' : 'inline')
            .text((d) => d.count);


    const parentBubbles = svg
        .selectAll('.cluster')
        .data(parents, (d) => d.data.name)
        .join('circle')
        .attr("class", "cluster")
        .attr("fill", 'light-gray')
        .attr("fill-opacity", 0.05)
        .attr("stroke-width", 5)
        .style("display", (d) => bubbleLayout === BubbleLayout.CLUSTER && (!focus || (selectedCluster && selectedCluster.name === d.data.name)) ? 'inline' : 'none')
        .on("mouseover", focus ? null : function() { d3.select(this).attr("stroke", Colors.cluster); })
        .on("mouseout", function() { d3.select(this).attr("stroke", null); })
        .on("click", (event, d) => {
            setFocus(d);
        });

    const parentLabels =
        svg.selectAll(".parentlabel")
            .data(parents, (d) => d.data.name)
            .join("text")
            .attr("class", "parentlabel")
            .style("text-anchor", "middle")
            .style("font", `${fontSize}px ${fontFamily}`)
            .attr("transform", (d) => `translate(${d.x},${d.y})`)
            .style("display", bubbleLayout === BubbleLayout.CLUSTER && !focus ? 'inline' : 'none')
            .text((d) => cutIfNeeded(d.data.name));


    useEffect(() => {
        if (bubbleLayout === BubbleLayout.CLUSTER) {
            if (!focus && prevFocus) {
                console.log(prevFocus);
                svg.transition()
                    .duration(animationDuration)
                    .tween("zoom", d => {
                        const i = d3.interpolateZoom([prevFocus.x, prevFocus.y, prevFocus.r * 3], [width / 2, height / 2, width]);
                        return t => zoomTo(i(t), width / 2, height / 2);
                    });
                setSelectedCluster(undefined);

            } else if (focus) {
                svg.transition()
                    .duration(animationDuration)
                    .tween("zoom", d => {
                        const i = d3.interpolateZoom([width / 2, height / 2, width], [focus.x, focus.y, focus.r * 3]);
                        return t => zoomTo(i(t), width / 2, height / 2);
                    });

                const clusterHashtags = focus.children.map((d) => d.data.name);
                setSelectedCluster({
                    'name': focus.data.name,
                    'hashtags': clusterHashtags
                });
                setPrevFocus(focus);
            }
        }
    }, [focus])

    useEffect(() => {
        if(!selectedCluster) {
            setFocus(undefined)
        }
    }, [selectedCluster])



    function zoomTo(v, offsetWidth, offsetHeight) {
        const k = width/ v[2];
        labels.attr("transform", d => `translate(${(d.x-v[0])*k+offsetWidth},${(d.y-v[1])*k+offsetHeight})`);
        parentLabels.attr("transform", d => `translate(${(d.x-v[0])*k+offsetWidth},${(d.y-v[1])*k+offsetHeight})`);
        bubbles.attr("r", d => d.r*k );
        bubbles.attr("transform", (d) => `translate(${(d.x-v[0])*k+offsetWidth},${(d.y-v[1])*k+offsetHeight})`);
        parentBubbles.attr("r", d => d.r*k );
        parentBubbles.attr("transform", (d) => `translate(${(d.x-v[0])*k+offsetWidth},${(d.y-v[1])*k+offsetHeight})`);

    }

    useEffect(() => {
        if(selectedId !== undefined) {
            const path = process.env.PUBLIC_URL + '/data/clusters/' + selectedId + '.json';

            d3.json(path).then(data => {
                setData(data);
                setSelectedCluster(undefined);
                setFocus(undefined);
                setPrevFocus(undefined);
            });
        } else {
            setData([]);
        }
    }, [selectedId]);


    useEffect(() => {
        console.log('updating layout');
        if (bubbleLayout === BubbleLayout.COUNT || bubbleLayout === BubbleLayout.UNIQUENESS) {
            setSelectedCluster(undefined);
            setFocus(undefined);
            setPrevFocus(undefined);
            setParents([]);
            if (bubbleLayout === BubbleLayout.COUNT) {
                data.sort(function(a, b) {
                    return b.radius - a.radius;
                });

            } else {
                data.sort(function(a, b) {
                    return b.rank - a.rank;
                });
            }

            const visibleDataPoints = data.slice(0, nx*ny);
            const sortedHashtags = visibleDataPoints.map(d => d.hashtag);
            const newBubbles = visibleDataPoints.map((d) => {
                    const index = sortedHashtags.indexOf(d.hashtag);
                    const x = getX(index);
                    const y = getY(index);
                    const xPos = xScale(x);
                    const yPos = yScale(y);
                    return {
                        'x': xPos,
                        'y': yPos,
                        ...d
                    }
                });
            setVisibleBubbles(newBubbles);


        } else {
            const dataPointsInCluster = data.filter((d) => {
                    return d.cluster !== "";
                });

            const clustersByName =
                dataPointsInCluster.reduce(function(memo, x) {
                    if (!memo[x['cluster']]) { memo[x['cluster']] = []; }
                    memo[x['cluster']].push({'name': x.hashtag, 'count': x.count, 'radius': x.radius});
                    return memo;
                }, {});

            const clustersArray = [];

            for (const [key, value] of Object.entries(clustersByName)) {
                clustersArray.push({
                    'name': key,
                    'children': value
                })
            }

            const clustersData = {
                'name': 'root',
                'children': clustersArray
            };

            const root = d3.pack()
                .size([width - marginLeft - marginRight, height - marginTop - marginBottom])
                .padding(padding)
                (d3.hierarchy(clustersData)
                    .sum(d => d.radius)
                    .sort((a, b) => b.radius - a.radius));


            const descendants = root.descendants().slice(1);
            const children = descendants.filter(node => !node.children);
            const nodeValues = {};
            children.map((node) => {
                nodeValues[node.data.name] = {'x': node.x , 'y': node.y , 'r': node.r};
            })

            const newBubbles = dataPointsInCluster.map((d) => {
                return {
                    'x': nodeValues[d.hashtag].x,
                    'y': nodeValues[d.hashtag].y,
                    'r': nodeValues[d.hashtag].r,
                    ...d
                }
            });
            setVisibleBubbles(newBubbles);
            setParents(descendants.filter(node => node.children));
        }
    },[bubbleLayout, data]);




    useEffect(()=> {
        if (bubbleLayout === BubbleLayout.COUNT || bubbleLayout === BubbleLayout.UNIQUENESS) {
            bubbles.transition()
                .duration(animationDuration)
                .attr("transform", (d) => `translate(${d.x+marginLeft},${d.y+marginTop})`)

            labels.transition()
                .duration(animationDuration)
                .attr("transform", (d) => `translate(${d.x+marginLeft},${d.y+marginTop  +fontSize /2})`)

            labelsSmall.transition()
                .duration(animationDuration)
                .attr("transform", (d) => `translate(${d.x+marginLeft},${d.y+marginTop  + xScale.bandwidth()/2 + fontSize })`)
        } else {

            bubbles.transition()
                .duration(animationDuration)
                .attr("r", (d => d.r))
                .attr("transform", (d) => `translate(${d.x},${d.y})`);

            labels.transition()
                .duration(animationDuration)
                // .attr("r", (d => d.r))
                .attr("transform", (d) => `translate(${d.x},${d.y})`);

            labelsSmall.transition()
                .duration(animationDuration)
                .attr("transform", (d) => `translate(${d.x+marginLeft},${d.y+marginTop +fontSize/2 })`)


        }
    },[visibleBubbles])


    useEffect(() => {
        parentBubbles.transition()
            .duration(animationDuration)
            .attr("r", (d) => d.r)
            .attr("transform", (d) => `translate(${d.x},${d.y})`);

        parentLabels.transition()
            .duration(animationDuration)
            // .attr("r", (d => d.r))
            .attr("transform", (d) => `translate(${d.x},${d.y})`);

    },[parents])


    return (
            <div id="clusterschart">
                <svg ref={d3Chart}/>
            </div>
    );
}
export default ClustersChart;