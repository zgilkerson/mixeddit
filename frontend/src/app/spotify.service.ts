import { Injectable } from '@angular/core';
import { HttpClient, HttpErrorResponse } from '@angular/common/http';

import { catchError } from 'rxjs/operators';

import { MixedditErrorService } from './mixeddit-error.service';

@Injectable()
export class SpotifyService {

  api = 'api/spotify/';

  constructor(private http: HttpClient,
              private mixedditErrorService: MixedditErrorService) { }

  getLoggedIn() {
    return this.http.get(this.api + 'check_logged_in/');
  }

  putPlaylistReplace(mixedditValue) {
    return this.http.put(this.api + 'playlist_replace/', mixedditValue)
      .pipe(
        catchError(this.mixedditErrorService.handleError)
      );
  }
}
