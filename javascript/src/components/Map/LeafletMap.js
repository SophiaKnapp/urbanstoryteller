import {MapContainer, TileLayer, GeoJSON} from 'react-leaflet'
import React, {useState} from "react";
import {Colors} from "../../assets/colors";
import {MapState} from "../../App";


const LeafletMap = ({potatoesWithOpacity, setSelectedId, selectedId, mapState})=>{

    const fillColor = (isSelected, isHover, state) => {
        switch (state) {
            case MapState.postCount:
                switch (isSelected) {
                    case true:
                        return Colors.district;
                    default:
                        return Colors.posts;
                }
            case MapState.hashtags:
                switch (isSelected) {
                    case true:
                        return Colors.district;
                    default:
                        return Colors.hashtags;
                }
        }
        return '';
    }

    const [onHover, setOnHover] = useState('');
    const highlightFeature = (e=> {
        setOnHover(e.target.feature.id);
    });

    const selectFeature = (e=> {
        console.log('SELECT FEATURE');
        console.log(e.target.feature.id);
        console.log(e.target.feature.id === selectedId);
        if (e.target.feature.id === selectedId) {
            setSelectedId(undefined);
        } else {
            setSelectedId(e.target.feature.id);
        }
    });

    const resetHighlight= (e => {
        setOnHover('');
    })

    const onEachFeature= (feature, layer)=> {
        layer.on({
            mouseover: highlightFeature,
            click: selectFeature,
            mouseout: resetHighlight,
        });
    }

    const style = (feature => {
        return ({
            fillColor: fillColor(feature.id === selectedId, feature.id === onHover, mapState),
            weight: feature.id === selectedId || feature.id === onHover ? 3 : 1,
            opacity: 1,
            color: fillColor(feature.id === selectedId, feature.id === onHover, mapState),
            fillOpacity: feature.id === onHover ? 1 : feature.properties.opacity,
        });
    });
    const geojsonLayer = potatoesWithOpacity.map(feature=>{
        return(feature);
    });

    return(
        <div className='container'>
            <div className="">
                <div className="">
                    <MapContainer zoom={11}
                                  scrollWheelZoom={true}
                                  center={[48.1374, 11.750]}>
                        <TileLayer
                            url="https://api.mapbox.com/styles/v1/leonie35/cl6jd9wxa005d14nkzj8cvw22/tiles/256/{z}/{x}/{y}@2x?access_token=pk.eyJ1IjoibGVvbmllMzUiLCJhIjoiY2w2Z2xxcjMwMDAyczNjcGt6MjU5Z2xwNyJ9.ZwNjh5NstxlW2iTC7HE1cg"

                        />
                        {geojsonLayer && (
                            <GeoJSON data={geojsonLayer}
                                     style={style}
                                     onEachFeature={onEachFeature}
                            />
                        )}
                    </MapContainer>
                </div>
            </div>
        </div>
    )
}
export default LeafletMap;