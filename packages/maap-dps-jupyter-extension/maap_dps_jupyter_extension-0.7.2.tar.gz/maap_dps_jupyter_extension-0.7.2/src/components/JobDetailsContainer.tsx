import React from 'react'
import { Nav, Tab } from 'react-bootstrap'
import { useSelector } from 'react-redux'
import { GeneralJobInfoTable } from './GeneralJobInfoTable'
import { InputsJobInfoTable } from './InputsJobInfoTable'
import { selectJobs } from '../redux/slices/jobsSlice'
import { MetricsJobInfoTable } from './MetricsJobInfoTable'
import '../../style/JobDetailsContainer.css'
import { ErrorsJobInfoTable } from './ErrorsJobInfoTable'
import { OutputsJobInfoTable } from './OutputsJobInfoTable'

export const JobDetailsContainer = ({ jupyterApp }): JSX.Element => {

    // Redux
    const { selectedJob } = useSelector(selectJobs)

    return (
        <div className="job-details-container">
            <h2>Job Details</h2>
            <Tab.Container id="left-tabs-example" defaultActiveKey="general">
                <Nav variant="pills" className="nav-menu">
                    <Nav.Item>
                        <Nav.Link eventKey="general">General</Nav.Link>
                    </Nav.Item>
                    <Nav.Item>
                        <Nav.Link eventKey="inputs">Inputs</Nav.Link>
                    </Nav.Item>
                    <Nav.Item>
                        <Nav.Link eventKey="outputs">Outputs</Nav.Link>
                    </Nav.Item>
                    <Nav.Item>
                        <Nav.Link eventKey="errors">Errors</Nav.Link>
                    </Nav.Item>
                    <Nav.Item>
                        <Nav.Link eventKey="metrics">Metrics</Nav.Link>
                    </Nav.Item>
                </Nav>
                <Tab.Content className="content-padding">
                    <Tab.Pane eventKey="general">
                        {selectedJob ? <GeneralJobInfoTable /> : <div className='subtext'>No job selected</div>}
                    </Tab.Pane>
                    <Tab.Pane eventKey="inputs">
                        {selectedJob ? <InputsJobInfoTable /> : <span className='subtext'>No job selected</span>}
                    </Tab.Pane>
                    <Tab.Pane eventKey="outputs">
                        {selectedJob ? <OutputsJobInfoTable jupyterApp={jupyterApp}/> : <span className='subtext'>No job selected</span>}
                    </Tab.Pane>
                    <Tab.Pane eventKey="errors">
                        {selectedJob ? <ErrorsJobInfoTable /> : <span className='subtext'>No job selected</span>}
                    </Tab.Pane>
                    <Tab.Pane eventKey="metrics">
                        {selectedJob ? <MetricsJobInfoTable /> : <span className='subtext'>No job selected</span>}
                    </Tab.Pane>
                </Tab.Content>
            </Tab.Container>
        </div>
    )
}