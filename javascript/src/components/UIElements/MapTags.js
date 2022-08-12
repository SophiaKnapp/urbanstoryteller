
import { Tag, Tooltip, Row } from 'antd';
import React, { useEffect, useRef, useState } from 'react';
import {Colors} from "../../assets/colors";




// export default App;
// .site-tag-plus {
//     background: #fff;
//     border-style: dashed;
// }
// .edit-tag {
//     user-select: none;
// }
// .tag-input {
//     width: 78px;
//     margin-right: 8px;
//     vertical-align: top;
// }

const TagType = {
    DISTRICT: 'district',
    HASHTAG: 'hashtag',
    CLUSTER: 'cluster'
}

const MapTags = ({selectedHashtags, selectedId, selectedCluster, setSelectedId, setSelectedCluster, setSelectedHashtags}) => {

    // const [selectedHashtags, setSelectedHashtags] = useState(['Unremovable', 'Tag 2', 'Tag 3']);
    // const [inputVisible, setInputVisible] = useState(false);
    // const [inputValue, setInputValue] = useState('');
    // const [editInputIndex, setEditInputIndex] = useState(-1);
    // const [editInputValue, setEditInputValue] = useState('');
    // const inputRef = useRef(null);
    // const editInputRef = useRef(null);
    // useEffect(() => {
    //     if (inputVisible) {
    //         inputRef.current?.focus();
    //     }
    // }, [inputVisible]);
    // useEffect(() => {
    //     editInputRef.current?.focus();
    // }, [inputValue]);

    const handleClose = (removedTag, tagType) => {
        switch (tagType) {
            case TagType.DISTRICT:
                setSelectedId(undefined);
                break;
            case TagType.HASHTAG:
                let newHashtags = [...selectedHashtags];
                newHashtags = newHashtags.filter(v => v !== removedTag);
                setSelectedHashtags(newHashtags);
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
                    closable={true} // TODO: always closable
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