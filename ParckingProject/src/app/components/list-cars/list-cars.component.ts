import { Component } from '@angular/core';
import { CarService } from 'src/app/services/car.service';
import { ActivatedRoute, Router } from '@angular/router';
import { MatriculeModel } from '../add-car/car.module';

@Component({
  selector: 'app-list-cars',
  templateUrl: './list-cars.component.html',
  styleUrls: ['./list-cars.component.css']
})
export class ListCarsComponent {
  title = 'Liste des Voitures'
  cars!:MatriculeModel[];
  displayedColumns: string[] = ['numero matricule','Nom client', 'CNI client','date enregistremnt','etat','Rapport'];
  dataSource!:MatriculeModel[]
  searchQuery: string = '';
  constructor(private myservice:CarService,private activatedRouter:ActivatedRoute,
    private router:Router){
    this.myservice.getAllcars().subscribe(
  
        (data)=>{
  
          this.cars = data;
          this.dataSource = this.cars;
          
        }
  
  
    );
  }
  searchCars() {
    if (this.searchQuery) {
      this.dataSource = this.cars.filter(
        (car) => car.code_matricule.toLowerCase().includes(this.searchQuery.toLowerCase())
      );
    } else {
      this.dataSource = this.cars;
    }
  }

  clearSearch() {
    this.searchQuery = '';
    this.dataSource = this.cars;
  }
  

}
