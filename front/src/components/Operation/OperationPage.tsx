import { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
//import "../styles/stylesForOperationPage.css"
import { GetOperation} from "./GetOperation";

interface  Operation {
    id: number;
    img_src: string;
    name: string;
    description: string;
    status: string;
    image: string;
}

const Operation = () => {
    const { id } = useParams(); // Получаем значение параметра :id из URL
    const OperationId = id ? parseInt(id, 10) : null; // Преобразование в число или null

    const [Operation_, setOperation] = useState<Operation | null>(null);

    useEffect(() => {
        if (OperationId !== null) {
            GetOperation(OperationId)
                .then((result:any) => {
                    if (result.data !== null) {
                        setOperation(result.data[0]);
                    }
                })
                .catch((error:any) => {
                    console.error('Error:', error);
                });
        }
    }, [OperationId]);

    if (!Operation_) {
        return <div>Loading...</div>;
    }

    return (<>
        <main>
  <div className="card">
    <div className="card__name">
      <div className="icon">
        <a href="http://0.0.0.0:8080/"><i className="fa fa-arrow-left"></i></a>
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css">
      </div>
      
    </div>
    <div class="card__body">
      <div class="half">
        <div class="featured_text">
          <h1>{{name}}</h1>
          <p class="sub">Бинарная операция:</p>
        </div>
        <div class="image">
          <img src={{img}} alt="">
        </div>
      </div>
      <div class="half">
        <div class="description">
          <p>{{text}}</p>
        </div>
        <span class="stock"><i class="fa fa-pen"></i></span><!-- can add pink text here-->
        <div class="reviews">
          <ul class="stars">
            <li><i class="fa fa-star"></i></li> <!--add features here-->
            <li><i class="fa fa-star"></i></li>
            <li><i class="fa fa-star"></i></li>
            <li><i class="fa fa-star"></i></li>
            <li><i class="fa fa-star-o"></i></li>
          </ul>
          <span></span><!--add reviews count here-->
        </div>
      </div>
    </div>
    <div class="card__footer">
      <div class="recommend">
        <p>Recommended by</p>
        <h3>Allochka Danielyan</h3>
      </div>
      <div class="action">
        <button type="button">Добавить в заявку</button>
      </div>
    </div>
  </div>
</main>
        <div className="container-1">
            <span>
                <img style={{ width: '30%', height: 'auto' }} src={Operation_.image} alt="" />
            </span>

            <h1 className="short_text">{Operation_.name}</h1>

            <hr className="line" />

            <div className="container">
                <p className="info">
                {Operation_.description}
                </p>
            </div>
        </div>
        </>
    );
};

export default Operation;