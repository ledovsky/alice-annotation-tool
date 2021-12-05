import React from 'react';
import { BrowserRouter as Router, Switch, Route, Redirect } from 'react-router-dom';
import { ToastContainer } from 'react-toastify';

import HomePage from './components/HomePage';
import DocsPage from './components/DocsPage';
import Login from './containers/LoginContainer';
import Navbar from './containers/NavbarContainer';
import Footer from './components/Footer';
import Datasets from './containers/DatasetsContainer';
import DatasetView from './containers/DatasetViewContainer';
import SubjectView from './containers/SubjectViewContainer';
import ComponentAnnotation from './containers/ComponentAnnotationContainer';
import AnnotationList from './containers/AnnotationListContainer';
import Downloads from './containers/DownloadsContainer';
import NotFound from './components/NotFound';


function App() {

  console.log("App component");

  return (
    <React.Fragment>
      <div className="flex-auto">
        <Router>
          <Navbar />
          <Switch>
            <Route exact path="/" component={HomePage} />
            <Route path="/login" component={Login} />
            <Route exact path="/datasets" component={Datasets} />
            <Route exact path="/datasets/:dataset_id" component={DatasetView} />

            <Route exact path="/subjects/:subject_id" component={SubjectView} />
            <Route exact path="/ic/:ic_id/annotate" component={ComponentAnnotation} />

            {/* Delete */}
            <Route exact path="/ic/:ic_id/" component={AnnotationList} />


            <Route exact path="/downloads" component={Downloads} />
            <Route path="/docs" component={DocsPage} />
            <Route exact path="/404" component={NotFound} />
            <Redirect to="/404" />
          </Switch>
        </Router>
        <ToastContainer />
      </div>
      <Footer/>
    </React.Fragment>
  );
}

export default App;
