import { Component, OnInit } from '@angular/core';
import { FormControl } from '@angular/forms';

@Component({
  selector: 'app-navbar',
  templateUrl: './navbar.component.html',
  styleUrls: ['./navbar.component.css']
})
export class NavbarComponent implements OnInit {
  lights = new FormControl();

  constructor() {
    this.themeSwitched();
  }

  ngOnInit() {
  }

  themeSwitched() {
    this.lights.valueChanges.forEach(
      (value: boolean) => console.log(value)
    );
  }
}
