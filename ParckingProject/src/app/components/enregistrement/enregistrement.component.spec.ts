import { ComponentFixture, TestBed } from '@angular/core/testing';

import { EnregistrementComponent } from './enregistrement.component';

describe('EnregistrementComponent', () => {
  let component: EnregistrementComponent;
  let fixture: ComponentFixture<EnregistrementComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ EnregistrementComponent ]
    })
    .compileComponents();

    fixture = TestBed.createComponent(EnregistrementComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
