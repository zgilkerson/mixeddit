import { Component } from '@angular/core';
import { Http, Response } from '@angular/http';
import { Observable } from 'rxjs/Observable';
import 'rxjs/add/operator/toPromise';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent {
  title = 'app';

  constructor(private http: Http) {}

  public me() {
    const url = 'https://localhost/spotify/hello/';
    this.http.get(url).toPromise().then((res) => {
      console.log(res.json());
    });
  }

  public login() {
    const url = 'https://localhost/spotify/login/';
    this.http.get(url).toPromise().then((res) => {
      console.log(res.json());
    });
  }
}
