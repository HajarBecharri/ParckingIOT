import { Component } from '@angular/core';
import { CarModule } from '../add-car/car.module';
import { CarService } from '../../services/car.service';
import { ActivatedRoute, Router } from '@angular/router';
import { UserModule } from '../user/user.module';
import { UserService } from 'src/app/services/user.service';

export interface PeriodicElement {
  name: string;
  position: number;
  weight: number;
  symbol: string;
}

const ELEMENT_DATA: PeriodicElement[] = [
  {position: 1, name: 'Hydrogen', weight: 1.0079, symbol: 'H'},
  {position: 2, name: 'Helium', weight: 4.0026, symbol: 'He'},
  {position: 3, name: 'Lithium', weight: 6.941, symbol: 'Li'},
  {position: 4, name: 'Beryllium', weight: 9.0122, symbol: 'Be'},
  {position: 5, name: 'Boron', weight: 10.811, symbol: 'B'},
  {position: 6, name: 'Carbon', weight: 12.0107, symbol: 'C'},
  {position: 7, name: 'Nitrogen', weight: 14.0067, symbol: 'N'},
  {position: 8, name: 'Oxygen', weight: 15.9994, symbol: 'O'},
  {position: 9, name: 'Fluorine', weight: 18.9984, symbol: 'F'},
  {position: 10, name: 'Neon', weight: 20.1797, symbol: 'Ne'},
];
@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.css']
})
export class HomeComponent {
  
  cars!:CarModule[];
  adcar=false;
  displayedColumns: string[] = ['hp','model', 'marque','delete','update'];
  dataSource!:CarModule[]
  user!:UserModule
  constructor(private myservice:CarService,private userservice:UserService,private activatedRouter:ActivatedRoute,
    private router:Router){
      userservice.userObservable.subscribe((newuser)=>
      this.user=newuser)
    this.myservice.getAllcars().subscribe(
  
        (data)=>{
  
          this.cars = data;
          this.dataSource = this.cars;
          
        }
  
  
    );
  }

  
  addcar(){
    this.router.navigateByUrl("addCar")
  }

  logout(){
    this.userservice.logout()
  }
}

