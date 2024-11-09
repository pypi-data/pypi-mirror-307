import React, { useState } from 'react'
import SplitPane, { Pane } from 'split-pane-react';
import 'split-pane-react/esm/themes/default.css';
import { JobDetailsContainer } from './JobDetailsContainer'
import { JobsOverviewContainer } from './JobsOverviewContainer'
// import { JobsContainerActions } from '../redux/slices/JobsContainerSlice'
// import { useDispatch } from 'react-redux'
import { MdArrowDropUp, MdArrowDropDown } from 'react-icons/md';

export const JobsView = ({ jupyterApp }): JSX.Element => {

    const [sizes, setSizes] = useState([100, '5%']);


    const sash = () => {
        return <div className='sash-resizer'>
                <MdArrowDropUp className='sash-resizer-up' onClick={() => setSizes([0, 100])}/>
                <MdArrowDropDown className='sash-resizer-down' onClick={() => setSizes([100, 0])}/>
            </div>
    }

    return (
        <div style={{ height: '80vh' }}>
            <SplitPane
                sashRender={sash}
                resizerSize={2}
                //sashClassName='sash-resizer'
                split='horizontal'
                sizes={sizes}
                onChange={setSizes}
            >
                <Pane maxSize='100%' style={{ overflow: 'scroll' }}>
                    <JobsOverviewContainer jupyterApp={jupyterApp} />
                </Pane>
                <Pane maxSize='100%' style={{ overflow: 'scroll' }}>
                    <JobDetailsContainer jupyterApp={jupyterApp} />
                </Pane>
            </SplitPane>
        </div>
    )
}