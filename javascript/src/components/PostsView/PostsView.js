import React, {useEffect ,useState} from 'react';
import '../../App.css';
import * as d3 from 'd3';
import { IGEmbed } from 'react-ig-embed';
import {Col, Row, Pagination} from "antd";

const PostsView = ({selectedId, selectedHashtags, selectedCluster}) => {

    const [urls, setUrls] = useState([]);
    const [cols, setCols] = useState(<></>);
    const [currentPage, setCurrentPage] = useState(0);
    const [nPages, setNPages] = useState(1);

    const postsPerPage = 8;
    const [description, setDescription] = useState('');

    const getSortedIndices = (obj) => {
        const sortedObj = Object.keys(obj).sort((a, b) => obj[b] - obj[a]);
        return sortedObj;
    };

    const getValuesForHashtags = (queryHashtags, margin, hashtagsPosts, nPostsToCheck) => {
        const values = {};

        for (let i = 0; i < nPostsToCheck; i++) {
            const hashtags = hashtagsPosts[i];

            if (hashtags) {
                const hashtagsString = hashtags.replace(/'/g, '"');
                const hashtagsList = JSON.parse(hashtagsString);
                const nSelected = queryHashtags.filter(value => hashtagsList.includes(value)).length;
                if (nSelected >= margin) {
                    values[i] = nSelected / hashtagsList.length;
                }
            }
        }
        return values;
    }

    const getPosts = (selectedHashtags, selectedClusterHashtags, data) => {
        const maxN = 10000;
        let indices = [];
        const hashtagsPosts = data['hashtags'];

        const postCount = Object.keys(hashtagsPosts).length;
        const nPostsToCheck = Math.min(postCount, maxN);

        if (selectedHashtags.length > 0 && selectedClusterHashtags.length === 0) {
            const values = getValuesForHashtags(selectedHashtags, 1, hashtagsPosts, nPostsToCheck);
            const maxIndices = getSortedIndices(values);
            indices = maxIndices;
        } else if (selectedHashtags.length === 0 && selectedClusterHashtags.length > 0) {
            const values = getValuesForHashtags(selectedClusterHashtags, 2, hashtagsPosts, nPostsToCheck);
            const maxIndices = getSortedIndices(values);
            indices = maxIndices;
        } else if (selectedHashtags.length > 0 && selectedClusterHashtags.length > 0) {
            const clusterValues = getValuesForHashtags(selectedClusterHashtags, 2, hashtagsPosts, nPostsToCheck);
            let selectedHashtagsWithoutCluster = [...selectedHashtags].filter((hashtag) => !selectedClusterHashtags.includes(hashtag));
            const hashtagsValues = getValuesForHashtags(selectedHashtagsWithoutCluster, 1, hashtagsPosts, nPostsToCheck);
            const resultKeys = Object.keys(hashtagsValues).filter((k) => Object.keys(clusterValues).includes(k));
            const valuesSum = {};
            resultKeys.map((key) => {
                valuesSum[key] = hashtagsValues[key] + clusterValues[key]
            });
            indices = getSortedIndices(valuesSum);

        } else {
            indices = Array.from({length: nPostsToCheck}, (x, i) => i);
        }

        const result = [];
        for (let i=0; i < indices.length; i++) {
            const url = data.post_url[indices[i]]
            if (url) {
                result.push(url);
            }
        }
        return result;
    }

    const getText = (selectedId, selectedHashtags, selectedCluster, urls) => {
        let text = '';

        if (urls.length > 0 ) {
            text+= 'Most liked posts';
        } else {
            text+= 'No posts found'
        };

        if (selectedId) {
            text += ' in #' + selectedId;
        } else {
            text += ' from all districts';
        }

        if (selectedHashtags.length === 1) {
            text += ' using #' + selectedHashtags[0];
        } else if (selectedHashtags.length > 1) {
            text += ' using #';
            let exceptLast = selectedHashtags.slice(0, selectedHashtags.length - 1);
            let hashtagsString = exceptLast.join(', #');
            hashtagsString += ' or #' + selectedHashtags[selectedHashtags.length - 1];
            text += hashtagsString;
        }

        if (selectedCluster) {
            text += ' related to story #' + selectedCluster.name;
        }

        return text;
    }

    useEffect( () => {

            let path = process.env.PUBLIC_URL + '/data/posts_json/city.json';
            if (selectedId !== undefined) {
                path = process.env.PUBLIC_URL + '/data/posts_json/' + selectedId + '.json';
            }
            d3.json(path).then(data => {
                const urls =  getPosts(selectedHashtags, selectedCluster ? selectedCluster.hashtags : [], data);
                setUrls(urls);

            })
    },
    [selectedId, selectedHashtags, selectedCluster]);

    useEffect(() => {
        setNPages(urls.length);
        const selectedUrls = urls.slice(currentPage*postsPerPage, (currentPage+1)*postsPerPage);
        setCols(selectedUrls.map(url => {
            return (
                <Col span={3} key={url + Math.random()}>
                    <IGEmbed url={url}/>
                </Col>
            )
        }));
        setDescription(getText(selectedId, selectedHashtags, selectedCluster, urls));

    }, [urls, currentPage])

    return (
        <div>
            <Row>
                {cols}
            </Row>
            <Row justify="space-between">
                <Col>
                    <div className="posts-title">
                        {description}
                    </div>
                </Col>
                <Col>
                    <Pagination size="small" total={nPages} defaultPageSize={postsPerPage} showQuickJumper={false} showSizeChanger={false} onChange={setCurrentPage}/>
                </Col>
            </Row>
        </div>
    );
}
export default PostsView;