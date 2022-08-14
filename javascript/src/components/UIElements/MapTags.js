import { Tag, Row } from 'antd';
import React, { useEffect, useState } from 'react';
import {Colors} from "../../assets/colors";

const TagType = {
    DISTRICT: 'district',
    HASHTAG: 'hashtag',
    CLUSTER: 'cluster'
}

const MapTags = ({selectedHashtags, selectedId, selectedCluster, setSelectedId, setSelectedCluster, removeHashtag}) => {

    const handleClose = (removedTag, tagType) => {
        switch (tagType) {
            case TagType.DISTRICT:
                setSelectedId(undefined);
                break;
            case TagType.HASHTAG:
                removeHashtag(removedTag)
                break;
            case TagType.CLUSTER:
                setSelectedCluster(undefined);
                break;

        }
    };

    const [tags, setTags] = useState([]);

    useEffect (() => {

        let newTags = [];
        if (selectedId) {
            newTags.push({
                'name': selectedId,
                'color': Colors.district,
                'type' : TagType.DISTRICT
            })
        }

        if (selectedCluster) {
            newTags.push({
                'name': selectedCluster.name,
                'color' : Colors.cluster,
                'type': TagType.CLUSTER
            })
        }

        if (selectedHashtags.length > 0) {
            selectedHashtags.map((hashtag) => {
                newTags.push({
                    'name': hashtag,
                    'color': Colors.hashtags,
                    'type' : TagType.HASHTAG
                })
            })
        }
        setTags(newTags);

    }, [selectedId, selectedHashtags, selectedCluster])


    return (
        <Row>
            {tags.map((tag) =>

                <Tag
                    className="edit-tag"
                    key={tag.name}
                    closable={true}
                    onClose={() => handleClose(tag.name, tag.type)}
                    style={{background: tag.color}}
                >
                    <span className="map-tag-text">
                        {'#' + tag.name}
                    </span>
                </Tag>
            )}
        </Row>
    );

}

export default MapTags;