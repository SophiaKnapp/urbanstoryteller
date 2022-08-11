// import { Input } from 'antd';
// import React from 'react';
// const { Option } = Select;

// const { Search } = Input;

import { PlusOutlined } from '@ant-design/icons';
import { Input, Tag, Tooltip } from 'antd';
import React, { useEffect, useRef, useState } from 'react';





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


const HashtagSelect = ({selectedHashtags, setSelectedHashtags}) => {

    // const [selectedHashtags, setSelectedHashtags] = useState(['Unremovable', 'Tag 2', 'Tag 3']);
    const [inputVisible, setInputVisible] = useState(false);
    const [inputValue, setInputValue] = useState('');
    const [editInputIndex, setEditInputIndex] = useState(-1);
    const [editInputValue, setEditInputValue] = useState('');
    const inputRef = useRef(null);
    const editInputRef = useRef(null);
    useEffect(() => {
        if (inputVisible) {
            inputRef.current?.focus();
        }
    }, [inputVisible]);
    useEffect(() => {
        editInputRef.current?.focus();
    }, [inputValue]);

    const handleClose = (removedTag) => {
        const newTags = selectedHashtags.filter((tag) => tag !== removedTag);
        console.log(newTags);
        setSelectedHashtags(newTags);
    };

    const showInput = () => {
        setInputVisible(true);
    };

    const handleInputChange = (e) => {
        setInputValue(e.target.value);
    };

    const handleInputConfirm = () => {
        if (inputValue && selectedHashtags.indexOf(inputValue) === -1) {
            setSelectedHashtags([...selectedHashtags, inputValue]);
        }

        setInputVisible(false);
        setInputValue('');
    };

    const handleEditInputChange = (e) => {
        setEditInputValue(e.target.value);
    };

    const handleEditInputConfirm = () => {
        const newTags = [...selectedHashtags];
        newTags[editInputIndex] = editInputValue;
        setSelectedHashtags(newTags);
        setEditInputIndex(-1);
        setInputValue('');
    };


    return (
        <>
            {selectedHashtags.map((tag, index) => {
                if (editInputIndex === index) {
                    return (
                        <Input
                            ref={editInputRef}
                            key={tag}
                            size="small"
                            className="tag-input"
                            value={editInputValue}
                            onChange={handleEditInputChange}
                            onBlur={handleEditInputConfirm}
                            onPressEnter={handleEditInputConfirm}
                        />
                    );
                }

                const isLongTag = tag.length > 20;
                const tagElem = (
                    <Tag
                        className="edit-tag"
                        key={tag}
                        closable={true} // TODO: always closable
                        onClose={() => handleClose(tag)}
                    >
            <span
                onDoubleClick={(e) => {
                    if (index !== 0) {
                        setEditInputIndex(index);
                        setEditInputValue(tag);
                        e.preventDefault();
                    }
                }}
            >
              {isLongTag ? `${tag.slice(0, 20)}...` : tag}
            </span>
                    </Tag>
                );
                return isLongTag ? (
                    <Tooltip title={tag} key={tag}>
                        {tagElem}
                    </Tooltip>
                ) : (
                    tagElem
                );
            })}
            {inputVisible && (
                <Input
                    ref={inputRef}
                    type="text"
                    size="small"
                    className="tag-input"
                    value={inputValue}
                    onChange={handleInputChange}
                    onBlur={handleInputConfirm}
                    onPressEnter={handleInputConfirm}
                />
            )}
            {!inputVisible && (
                <Tag className="site-tag-plus" onClick={showInput}>
                    <PlusOutlined /> Search for hashtags
                </Tag>
            )}
        </>
    );

}

export default HashtagSelect;