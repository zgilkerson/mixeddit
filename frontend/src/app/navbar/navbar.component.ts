import { Component, OnInit } from '@angular/core';
import { FormControl } from '@angular/forms';

import { LightsService } from '../lights.service';

@Component({
  selector: 'app-navbar',
  templateUrl: './navbar.component.html',
  styleUrls: ['./navbar.component.css'],
})
export class NavbarComponent implements OnInit {
  theme_toggle = new FormControl();

  constructor(private lightsService: LightsService) {
    this.themeSwitched();
  }

  ngOnInit() {
  }

  themeSwitched() {
    this.theme_toggle.valueChanges.forEach(
      (value: boolean) => {
        document.getElementById('body').classList.toggle('light-theme');
        this.lightsService.changeLight(value);
      }
    );
  }
}
