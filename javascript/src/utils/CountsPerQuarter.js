import React from "react";

import posts_users_stories from '../assets/posts_users_stories.json';
import getCount from "../assets/hashtag_frequencies";


const CountsPerQuarter = (selectedHashtags) => {
    const values = [];
    const potatoes = posts_users_stories.map((d) => d.quarter);
    // console.log(potatoes);
    //
    // // for (const i = 0; i< potatoes_users_stories.map; )

    potatoes.map((id) => {
        const json = getCount(id); // TODO: improve, make asyn
        const totalCount = json[id];

        let selectedHashtagsCount = 0;
        if (selectedHashtags.length > 0) {
            for (let j = 0; j < selectedHashtags.length; j++) {
                let hashtag = selectedHashtags[j];
                const count = json[hashtag];
                if (count !== undefined) {
                    selectedHashtagsCount += count;
                }
            }
        }
        values[id] = {
            "totalCount" : totalCount,
            "count" : selectedHashtags.length === 0 ? totalCount : selectedHashtagsCount,
            "relativeAmount": selectedHashtagsCount / totalCount
        }
    })
    return values;
}
export default CountsPerQuarter;