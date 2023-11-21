import React from 'react';
import { Link } from 'react-router-dom';
import AddButton from './addButton.tsx';
import "./OperationsPage.css";

interface Operation {
  pk: number;
  img_src: string;
  image: string;
  name: string;
  description: string;
  status: string;
 
}

const OperationCard: React.FC<{operationData: Operation}> = ({operationData}) => {
  console.log("operation card", operationData)
  return (<>
    <div className="my-card">
  <div className="face face1">
  
    <div className="content">
      
      <img src={operationData.img_src}/>
      <h3>{operationData.name}</h3>
    </div>
  </div>
  <div className="face face2">
    <div className="content">
      <div>
      <Link to={`/operation/${operationData.pk}`}>
                <AddButton/>
              </Link>
      </div>
    </div>
  </div>
</div>
</>
  )
}

export default OperationCard