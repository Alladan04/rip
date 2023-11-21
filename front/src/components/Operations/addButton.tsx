import  { Component } from 'react'
import { Button } from 'react-bootstrap'
//import "../styles/Podrobnee_button.scss"

export default class AddButton extends Component {
  render() {
    return (
        <Button variant="primary" className="podrobnee_button">Подробнее</Button>
    )
  }
}