import {useEffect, useState} from 'react'
import {GetFilteredOps, OpRes} from './GetOperations.ts'
// import "../styles/search_button.css"
// import {setGeographicalObjectData} from "../components/Main.tsx"


function SearchOperations({
    setOperationData,
    setTitleData,
}: {
setOperationData: (data: OpRes) => void;
setTitleData: (data: any) => void;
}) {
// Для фильтрации услуг
const [titleData, settitleData] = useState<string>('');

const handleFilterChange = (event: React.ChangeEvent<HTMLSelectElement | HTMLInputElement>) => {
    settitleData(event.target.value);
};

const handleFilterSubmit = async (event: React.FormEvent) => {
event.preventDefault();
};

useEffect(() => {
// Функция, которая будет выполнять фильтрацию данных
const fetchTitledData = async () => {
try {
const response = await GetFilteredOps(titleData);
setOperationData(response);
setTitleData(titleData);
} catch (error) {
console.error('Error filtering fines:', error);
}
};
// Вызываем фильтрацию данных при изменении filterKeyword
fetchTitledData();
// Этот useEffect будет выполнен при изменении filterKeyword или currentPage
}, [titleData]);


return (
<>
<div className="box">
  <form name="search" method = "get" onSubmit={handleFilterSubmit}>
      <input type="text" className="input" name="text" value = {titleData} 
      onChange={handleFilterChange}/>
  </form>
  <i className="fas fa-search"></i>

</div>
</>
);
};

export default SearchOperations;