import { Component } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { CarService } from 'src/app/services/car.service';
import { MatriculeModel } from '../add-car/car.module';

@Component({
  selector: 'app-parcking',
  templateUrl: './parcking.component.html',
  styleUrls: ['./parcking.component.css']
})
export class ParckingComponent {
  cars!:MatriculeModel[];
  displayedColumns: string[] = ['numero matricule','Nom client', 'CNI client','date enregistremnt','Rapport'];
  dataSource!:MatriculeModel[]
  searchQuery: string = '';
  constructor(private myservice:CarService,private activatedRouter:ActivatedRoute,
    private router:Router){
    this.myservice.getParckingcars().subscribe(
  
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
