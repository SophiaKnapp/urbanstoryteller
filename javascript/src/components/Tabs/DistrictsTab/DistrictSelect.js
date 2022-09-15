import { Select } from 'antd';
import React from 'react';
import posts_users_stories from '../../../assets/posts_users_stories.json';


const { Option } = Select;

const DistrictSelect = ({selectedId, setSelectedId}) => {
    let options = [];
    const quarters = posts_users_stories.map((d) => d.quarter);
    quarters.sort();

    for (let i = 0; i < quarters.length; i++) {
        options.push(<Option key={quarters[i]}>{'#' + quarters[i]}</Option>);
    }

    return (
        <Select
            showSearch
            optionFilterProp="children"
            style={{
                width: '100%',
            }}
            placeholder="Search for a district..."
            defaultValue={[]}
            onChange={setSelectedId}
            value={selectedId}
        >
            {options}
        </Select>
    );
}

export default DistrictSelect;