import {useState, useEffect} from 'react'

import {
    OpRes,
    GetFilteredOps
} from './GetOperations'
import OperationCard from './OperationCard.tsx';
import SearchOperation from './Search.tsx';
import './OperationsPage.css'
import Container from 'react-bootstrap/Container';
import Nav from 'react-bootstrap/Nav';
import Navbar from 'react-bootstrap/Navbar';

function Operations() {
    
    const [Operation_, setOperation] = useState<OpRes>({
        request_id: null,
        data:[],
    });

    const fetchData = async (tltleData: any) => {
        const data = await GetFilteredOps(tltleData);
        setOperation(data);
    };

    useEffect(() => {
        fetchData(tltleData);
    },[]);

    const setOperationData = (data: any) => {
        console.log('After filtration: ', data)
        setOperation(data);
    }

    const [tltleData, setTltleData] = useState('');

    console.log('lololo' , Operation_.data)
    return (
        <>
   
      <Navbar expand="lg"  bg=" #333"  style={{ maxHeight: '50px', marginBottom :'70px'}} data-bs-theme="dark" >
      <Container >
        <Navbar.Brand href="#home">BinaryOperations</Navbar.Brand>
        <Navbar.Toggle aria-controls="basic-navbar-nav" />
        <Navbar.Collapse id="basic-navbar-nav">
          <Nav className="me-auto">
            <Nav.Link href="#home">Операции</Nav.Link>
            <Nav.Link href="#link">Заявки</Nav.Link>
            
          </Nav>
        </Navbar.Collapse>
      </Container>
    </Navbar>
     
        <div className='search_in_menu'><SearchOperation setOperationData={setOperationData} setTitleData={setTltleData}/></div>

        <ul className="card-grid" >
            <div className="container flex-container">
            
                {Operation_.data.map((object) => (
                <OperationCard key = {object.pk} operationData={object}/>
                ))}
       
            </div>
            </ul>
        </>
    );
};

export default Operations;