import React, {useEffect, useState} from 'react';
import '../../App.css';
import {Col, Radio, Row, Layout} from "antd";
import ClustersChart from "./ClustersChart";
import DistrictSelect from "../UIElements/DistrictSelect";
import posts_users_stories from '../../assets/posts_users_stories.json';
import {Texts} from "../../assets/texts";
import ColorScaleUniqueness from "../UIElements/ColorScaleUniqueness";
import {Content, Footer} from "antd/es/layout/layout";

export const BubbleLayout = {
    COUNT: 'count',
    UNIQUENESS: 'uniqueness',
    CLUSTER: 'cluster'
}

const ClustersBox = ({selectedId, setSelectedId, selectedHashtags, addHashtag, removeHashtag, selectedCluster, setSelectedCluster}) => {


    const [stats, setStats] = useState(undefined);

    useEffect(() => {
        if (selectedId) {
            const row = posts_users_stories.find((d) => d.quarter === selectedId);
            setStats(row);
        } else {
            setStats(undefined);
        }

    }, [selectedId])


    const [bubbleLayout, setBubbleLayout] = useState(BubbleLayout.COUNT);


    return (
            <div className='sider-card'>
                <Row>
                    <Col span={24}>
                        <Row justify="space-between" >
                            <Col span={8}>
                                <DistrictSelect selectedId={selectedId} setSelectedId={setSelectedId} />
                            </Col>
                            <Col offset={1} span={15} >
                                <Radio.Group  disabled={selectedId===undefined} value={bubbleLayout} onChange={e => {
                                    setBubbleLayout(e.target.value);
                                }
                                }>
                                    <Radio.Button value={BubbleLayout.COUNT}>Most frequent</Radio.Button>
                                    <Radio.Button value={BubbleLayout.UNIQUENESS}>Most unique</Radio.Button>
                                    <Radio.Button value={BubbleLayout.CLUSTER}>Stories</Radio.Button>
                                </Radio.Group>
                            </Col>
                        </Row>
                    </Col>
                </Row>
                {!selectedId && (
                    <div>
                        <br/>
                        <div><b>{Texts.selectADistrict}</b></div>
                    </div>
                    )}
                    { stats && (
                        <>
                            <Layout>
                                <Content>
                                    <div className='graph-header-text'>
                                        {'Found '}
                                        <b>{stats.post_count}</b>
                                        {' posts in '}
                                        <b>{'#' + selectedId}</b>
                                        {', '}
                                        <b>{stats.users}</b>
                                        {' users talking about this, detected '}
                                        <b>{stats.stories}</b>
                                        {' stories.'}
                                    </div>
                                    <ClustersChart selectedId={selectedId} selectedHashtags={selectedHashtags} addHashtag={addHashtag} removeHashtag={removeHashtag} bubbleLayout={bubbleLayout} selectedCluster={selectedCluster} setSelectedCluster={setSelectedCluster}/>
                                </Content>
                                <Footer>
                                    <ColorScaleUniqueness/>
                                </Footer>
                            </Layout>
                        </>
                        )
                    }
                <Row>
                </Row>


            </div>
    )
}
export default ClustersBox;