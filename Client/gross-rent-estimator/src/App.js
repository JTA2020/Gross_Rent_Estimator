// import logo from './assets/logo.svg';
import React from 'react';
import './styles/App.css';
import {
  Container,
  Form,
  FormGroup,
  Label,
  Input,
  Button,
  Row,
  Col,
} from 'reactstrap';

function App() {

  //TODO: create clickhandler to receive input

  return (
    <>
      <Container className="border border-primary inputContainer">
        <Form>
          <FormGroup className="centerForm">
            <Label for="exampleText">Text Area</Label>
            <Input type="text" name="text" id="exampleText" className="w-50"/>
            <Button>Search</Button>
        </FormGroup>
        </Form>   
      </Container>
    </>
  );
}

export default App;
